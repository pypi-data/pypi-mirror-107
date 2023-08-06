# %% [markdown]
# # Dual Weighted Reisdual Estimate
#
# In this problem we revisit the Re-entrant Corner Problem but instead of
# a classical residual estimator we use a dual weighted residual estimator.
# The aim will be to refine the grid to reduce the error at a given point.
#
# Here we will consider the classic _re-entrant corner_ problem,
# \begin{align*}
# -\Delta u &= f, && \text{in } \Omega, \\
# u &= g, && \text{on } \partial\Omega,
# \end{align*}
# where the domain is given using polar coordinates,
# \begin{gather*}
# \Omega = \{ (r,\varphi)\colon r\in(0,1), \varphi\in(0,\Phi) \}~.
# \end{gather*}
# For the boundary condition $g$, we set it to the trace of the function $u$, given by
# \begin{gather*}
# u(r,\varphi) = r^{\frac{\pi}{\Phi}} \sin\big(\frac{\pi}{\Phi} \varphi \big)
# \end{gather*}

# %%
import matplotlib
matplotlib.rc( 'image', cmap='jet' )
import math
import numpy
import matplotlib.pyplot as pyplot
from dune.fem.plotting import plotPointData as plot
import dune.grid as grid
import dune.fem as fem
import dune.common as common
import dune.generator.algorithm as algorithm
from dune.fem.view import adaptiveLeafGridView as adaptiveGridView
from dune.fem.space import lagrange as solutionSpace
from dune.alugrid import aluConformGrid as leafGridView
from ufl import *
from dune.ufl import DirichletBC, expression2GF


# set the angle for the corner (0<angle<=360)
cornerAngle = 320.

# use a second order space
order = 2


# %% [markdown]
# We first define the domain and set up the grid and space.
# We need this twice - once for a computation on a globally refined grid
# and once for an adaptive one so we put the setup into a function:
#
# We first define the grid for this domain (vertices are the origin and 4
# equally spaced points on the unit sphere starting with (1,0) and
# ending at (cos(cornerAngle), sin(cornerAngle))
#
# Next we define the model together with the exact solution.

# %%
def setup():
    vertices = numpy.zeros((8, 2))
    vertices[0] = [0, 0]
    for i in range(0, 7):
        vertices[i+1] = [math.cos(cornerAngle/6*math.pi/180*i),
                         math.sin(cornerAngle/6*math.pi/180*i)]
    triangles = numpy.array([[2,1,0], [0,3,2], [4,3,0],
                             [0,5,4], [6,5,0], [0,7,6]])
    domain = {"vertices": vertices, "simplices": triangles}
    gridView = adaptiveGridView( leafGridView(domain) )
    gridView.hierarchicalGrid.globalRefine(2)
    space = solutionSpace(gridView, order=order)

    from dune.fem.scheme import galerkin as solutionScheme
    u = TrialFunction(space)
    v = TestFunction(space)
    x = SpatialCoordinate(space.cell())

    # exact solution for this angle
    Phi = cornerAngle / 180 * pi
    phi = atan_2(x[1], x[0]) + conditional(x[1] < 0, 2*pi, 0)
    exact = dot(x, x)**(pi/2/Phi) * sin(pi/Phi * phi)
    a = dot(grad(u), grad(v)) * dx

    # set up the scheme
    laplace = solutionScheme([a==0, DirichletBC(space, exact, 1)], solver="cg",
            parameters={"newton.linear.preconditioning.method":"jacobi"})
    uh = space.interpolate(0, name="solution")
    return uh, exact, laplace

uh, exact, laplace = setup()

# %% [markdown]
# Now we can setup the functional which will be $J(v)=v(P)$ where
# $P=(0.4,0.4)$ is some point in the computational domain at which we want
# to minimize the error. To compute the dwr estimator we need the solution
# to the dual problem with right hand side $J(\varphi_i)$ for all basis
# functions $\varphi_i$. This is not directly expressible in UFL and we
# therefore implement this using a small C++ function which we then export
# to Python:
#
# .. literalinclude:: laplace-dwr.hh

# %%
from dune.fem.scheme import galerkin as solutionScheme
spaceZ = solutionSpace(uh.space.grid, order=order+1)
u = TrialFunction(spaceZ)
v = TestFunction(spaceZ)
x = SpatialCoordinate(spaceZ)
a = dot(grad(u), grad(v)) * dx
dual = solutionScheme([a==0,DirichletBC(spaceZ,0)], solver="cg")
z = spaceZ.interpolate(0, name="dual")
zh = uh.copy(name="dual_h")
point = common.FieldVector([0.4,0.4])
pointFunctional = z.copy("dual_rhs")
eh = expression2GF( uh.space.grid, abs(exact-uh), order=order+1 )
computeFunctional = algorithm.load("pointFunctional", "laplace-dwr.hh",
            point, pointFunctional, eh)

# %% [markdown]
# %%
from dune.fem.space import finiteVolume as estimatorSpace
from dune.fem.operator import galerkin as estimatorOp

fvspace = estimatorSpace(uh.space.grid)
estimate = fvspace.interpolate([0], name="estimate")

u = TrialFunction(uh.space.as_ufl())
v = TestFunction(fvspace)
n = FacetNormal(fvspace.cell())
estimator_ufl = abs(div(grad(u)))*abs(z-zh) * v * dx +\
                abs(inner(jump(grad(u)), n('+')))*abs(avg(z-zh)) * avg(v) * dS
estimator = estimatorOp(estimator_ufl)
tolerance = 1e-6

# %% [markdown]
# Let us solve over a loop (solve,estimate,mark) and plot the solutions side by side.
# %%
h1error = dot(grad(uh - exact), grad(uh - exact))
fig = pyplot.figure(figsize=(10,10))
count = 0
errorVector    = []
estimateVector = []
dofs           = []
while True:
    laplace.solve(target=uh)
    if count%9 == 8:
        plot(uh, figure=(fig, 131+count//9), colorbar=False)
    pointFunctional.clear()
    error = computeFunctional(point, pointFunctional,eh)
    dual.solve(target=z, rhs=pointFunctional)
    zh.interpolate(z)
    estimator(uh, estimate)
    eta = sum(estimate.dofVector)
    dofs           += [uh.space.size]
    errorVector    += [error]
    estimateVector += [eta]
    if count%3 == 2:
        print(count, ": size=", uh.space.grid.size(0), "estimate=", eta, "error=", error)
    if eta < tolerance:
        break
    marked = fem.mark(estimate,eta/uh.space.grid.size(0))
    fem.adapt(uh) # can also be a list or tuple of function to prolong/restrict
    fem.loadBalance(uh)
    count += 1
plot(uh, figure=(fig, 131+2), colorbar=False)


# %% [markdown]
# Let's take a close up look of the refined region around the point of
# interest and the origin:
# %%
pyplot.close('all')
fig = pyplot.figure(figsize=(30,10))
plot(uh, figure=(fig, 131), xlim=(-0.5, 0.5), ylim=(-0.5, 0.5),
        gridLines="white", colorbar={"shrink": 0.75}, linewidth=2)
plot(uh, figure=(fig, 132), xlim=(-0.1, 0.5), ylim=(-0.1, 0.5),
        gridLines="white", colorbar={"shrink": 0.75}, linewidth=2)
plot(uh, figure=(fig, 133), xlim=(-0.02, 0.5), ylim=(-0.02, 0.5),
        gridLines="white", colorbar={"shrink": 0.75}, linewidth=2)

fig = pyplot.figure(figsize=(30,10))
from dune.fem.function import levelFunction
levels = levelFunction(uh.space.grid)
plot(levels, figure=(fig, 131), xlim=(-0.5, 0.5), ylim=(-0.5, 0.5),
        gridLines="white", colorbar={"shrink": 0.75})
plot(levels, figure=(fig, 132), xlim=(-0.1, 0.5), ylim=(-0.1, 0.5),
        gridLines="white", colorbar={"shrink": 0.75})
plot(levels, figure=(fig, 133), xlim=(-0.02, 0.5), ylim=(-0.02, 0.5),
        gridLines="white", colorbar={"shrink": 0.75})
