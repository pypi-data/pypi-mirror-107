# %% [markdown]
# # Advection: Discontinuous Galerkin Space-Time Method
# So far we have been using a method of lines in order to solve our
# PDE. In the following we show how to use Discontinuous Galerkin methods with
# upwind flux in a pace-time setting to solve an 2-dimensional advection
# problem
# \begin{align*}
# u_t + b\cdot\nabla u = 0
# \end{align*}
# with Dirichlet boundary conditions and initial condition
# \begin{align*}
# u(x,y) = \sin(\pi x) \sin(\pi y).
# \end{align*}
# Here $b = [b_x,b_y]$ a given vector of constant velocity.
# Then the exact solution reads
# \begin{align*}
# u(x,y,t) = \sin(\pi(x - b_x t)) \sin(\pi (y - \b_y t)).
# \end{align*}
# In the space-time ansatz, the temporal direction is discretized with a
# discontinuous Galerkin method as well. The simplest ansatz to translate the
# problem into a space-time problem in DUNE is to consider time as another
# dimension. Then the PDE reads
# \begin{align*}
# \tilde{b} \nabla \cdot u= 0
# \end{align*}
# with the vector of velocity $\tilde{b} = [b_x,b_y,1]$. Note that the only
# reasonale flux in the temproal direction is the uowind flux.
# %%

# %% [markdown]
# We solve the problem using the molGalerkin scheme and the dglagrange space.
# We start by importing all necessary packages and defining the problem and the
# setup for the ufl form.

# %%

import matplotlib
import numpy as np
matplotlib.rc( 'image', cmap='jet' )
#from dune.fem.space import dglagrange as dgSpace
from dune.fem.space import dglegendre as dgSpace
from dune.fem.scheme import molGalerkin as molGalerkin
from dune.ufl import Constant
from ufl import TestFunction, TrialFunction, SpatialCoordinate, FacetNormal
from ufl import dx, ds, grad, dot, inner, sin
from ufl import as_vector, avg, jump, dS, CellVolume, FacetArea, pi
try:
    from dune.spgrid import spAnisotropicGrid as leafGridView
except ImportError:
    from dune.grid import yaspGrid as leafGridView

from dune.grid import cartesianDomain
from dune.fem.function import uflFunction, integrate


#grid
Nx = 8
Nt = 8

t_end = 1
# %%
# spatial dimension
dim = 2

gridView = leafGridView(cartesianDomain([0]*(dim+1), [2]*dim + [t_end], [Nx]*dim + [Nt]))
if dim < 3:
    gridView.writeVTK(name='grid')

# %% [markdown]
# Note that so far the order is equal in all directions.

# %%
#order of the DG approximation
order = 2

if order >= 1:
    space    = dgSpace(gridView, order=order)
if order == 0:
    space    = dgSpace(gridView, order=order)

#setup for ufl form
u    = TrialFunction(space)
v    = TestFunction(space)
n    = FacetNormal(space)
he   = avg( CellVolume(space) ) / FacetArea(space)
x    = SpatialCoordinate(space)

# transport direction in x- and y-direction
b_coeff = [Constant(2/3,"b_x"), Constant(1/2,"b_y"), Constant(1/3,"b_z" )]

# %% [markdown]
# The velocity vector has a 1 in the third component for the temporal velocity:

# %%
b = as_vector([ b_coeff[i] for i in range(dim)] + [1.])

#define initial condition
def sol(xp,t):
    res = sin(pi*(xp[0]-b[0]*t))
    for i in range(1,dim):
        res *= sin(pi*(xp[i]-b[i]*t))
    return res

#define exact solution
def sol_st(xp):
    res = sin(pi*(xp[0]-b[0]*xp[dim]))
    for i in range(1,dim):
        res *= sin(pi*(xp[i]-b[i]*xp[dim]))
    return res

# %% [markdown]
# We plot the initial condition and solution at end point to compare it to the
# numerical solution. Since we know the exact solution, we can plot it as well.

# %%
#plot the initial condition, the solution at t_end and the 3D solution
ic = uflFunction(gridView, name='ic', order=space.order, ufl=sol(x,0))
if dim < 3:
    gridView.writeVTK('IC', pointdata=[ic])

sol_t = uflFunction(gridView, name='sol_t', order=space.order, ufl=sol(x,t_end))
if dim < 3:
    gridView.writeVTK('sol', pointdata=[sol_t])

#for boundary conditions
exact = uflFunction(gridView, name="exact", order=space.order+2, ufl=sol_st(x))
if dim < 3:
    gridView.writeVTK('exact', pointdata=[exact])

# %% [markdown]
# Now we write the 3D problem (space+time) in ufl form. Note that we use the
# upwind flux in all directions:

# %%
# upwind flux (same as LLF in this case)
hatb = (dot(b, n) + abs(dot(b, n)))/2.0

# b*div(u) = 0. Integration by parts yields
aInternal     = inner(-b*u, grad(v)) * dx
advSkeleton   = jump(hatb*u)*jump(v)*dS \
                +(hatb*u + (dot(b,n)-hatb)*exact)*v*ds

form = (aInternal + advSkeleton)

# %% [markdown]
# Finally, we can solve the problem using the discontinuous Galerkin method
# both in spatial and temporal direction and plot the numerical solution:

# %%
scheme = molGalerkin(form==0)

u_num = space.interpolate( 0, name="u_num")
#solve the problem using the molGalerkin scheme
scheme.solve(target=u_num)

errfct  = uflFunction(gridView, name="l2err", order=space.order, ufl=dot(u_num-exact, u_num-exact))
l2err   = np.sqrt(integrate(gridView, errfct, order=2+space.order*2))

print("L2-err: ", l2err)

#plot the numerical space-time solution
if dim < 3:
    gridView.writeVTK('num_sol', pointdata=[u_num])
