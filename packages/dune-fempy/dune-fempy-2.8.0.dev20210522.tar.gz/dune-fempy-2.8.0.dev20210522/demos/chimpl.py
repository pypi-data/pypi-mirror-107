# %% [markdown]
# # Cahn-Hilliard
# In this script we show how to use the $C^1$ non-conforming virtual
# element space to solve the Cahn-Hilliard equation. We use a fully implicit
# scheme here. You can find more details in <cite data-cite="VEM"></cite>

# %%
try:
    import dune.vem
except:
    import sys
    sys.exit(0)
import matplotlib
matplotlib.rc( 'image', cmap='jet' )
from matplotlib import pyplot
import math, random
from dune.grid import cartesianDomain, gridFunction
import dune.fem
from dune.fem.plotting import plotPointData as plot
from dune.fem.function import integrate, discreteFunction

from ufl import *
import dune.ufl

# %% [markdown]
# Grid and space construction - we use a cube grid here:
# %%
order        = 3
polyGrid = dune.vem.polyGrid( cartesianDomain([0,0],[1,1],[30,30]), cubes=True)
ncC1testSpaces = [ [0], [order-3,order-2], [order-4] ]
space = dune.vem.vemSpace(polyGrid, order=order, testSpaces=ncC1testSpaces)

# %% [markdown]
# To define the mathematical model, let $\psi\colon{\mathbb R} \rightarrow
# \mathbb{R}$ be defined as
# $\psi(x) = \frac{(1-x^2)^2}{4}$ and let $\phi(x) = \psi(x)^{\prime}$.
# The strong form for the solution
# $u\colon \Omega \times [0,T] \rightarrow {\mathbb R}$
# is given by
# \begin{align*}
# \partial_t u  - \Delta (\phi(u)-\epsilon^2 \Delta u) = 0
# \quad &\text{in} \ \Omega \times [0,T] ,\\
# u(\cdot,0) = u_0(\cdot)  \quad &\text{in} \ \Omega,\\
# \partial_n u = \partial_n \big( \phi(u) - \epsilon^2\Delta u \big) = 0
# \quad &\text{on} \ \partial \Omega \times [0,T].
# \end{align*}
#
# We use a backward Euler discretization in time and will fix the constant
# further down:

# %%
t     = dune.ufl.Constant(0,"time")
tau   = dune.ufl.Constant(0,"dt")
eps   = dune.ufl.Constant(0,"eps")
df_n  = discreteFunction(space, name="oldSolution") # previous solution
x     = SpatialCoordinate(space)
u     = TrialFunction(space)
v     = TestFunction(space)

H     = lambda v: grad(grad(v))
laplace = lambda v: H(v)[0,0]+H(v)[1,1]
a     = lambda u,v: inner(H(u),H(v))
b     = lambda u,v: inner( grad(u),grad(v) )
W     = lambda v: 1/4*(v**2-1)**2
dW    = lambda v: (v**2-1)*v

equation = ( u*v + tau*eps*eps*a(u,v) + tau*b(dW(u),v) ) * dx == df_n*v * dx

dbc = [dune.ufl.DirichletBC(space, 0, i+1) for i in range(4)]

# energy
Eint  = lambda v: eps*eps/2*inner(grad(v),grad(v))+W(v)

# %% [markdown]
# Next we construct the scheme providing some suitable expressions to stabilize the method

# %%
biLaplaceCoeff = eps*eps*tau
diffCoeff      = 2*tau
massCoeff      = 1
scheme = dune.vem.vemScheme(
                       [equation, *dbc],
                       solver=("suitesparse","umfpack"),
                       hessStabilization=biLaplaceCoeff,
                       gradStabilization=diffCoeff,
                       massStabilization=massCoeff,
                       boundary="derivative") # only fix the normal derivative = 0

# %% [markdown]
# To avoid problems with over- and undershoots we project the initial
# conditions into a linear lagrange space before interpolating into the VEM
# space:

# %%
def initial(x):
    h = 0.01
    g0 = lambda x,x0,T: conditional(x-x0<-T/2,0,conditional(x-x0>T/2,0,sin(2*pi/T*(x-x0))**3))
    G  = lambda x,y,x0,y0,T: g0(x,x0,T)*g0(y,y0,T)
    return 0.5*G(x[0],x[1],0.5,0.5,50*h)
initial = dune.fem.space.lagrange(polyGrid,order=1).interpolate(initial(x),name="initial")
df = space.interpolate(initial, name="solution")


# %% [markdown]
# Finally the time loop:

# %%
t.value = 0
eps.value = 0.05
tau.value = 1e-02

fig = pyplot.figure(figsize=(40,20))
count = 0
pos = 1
while t.value < 0.8:
    df_n.assign(df)
    info = scheme.solve(target=df)
    t.value += tau
    count += 1
    if count % 10 == 0:
        df.plot(figure=(fig,240+pos),colorbar=None,clim=[-1,1])
        energy = integrate(polyGrid,Eint(df),order=5)
        print("[",pos,"]",t.value,tau.value,energy,info,flush=True)
        pos += 1

# %% [markdown]
# For the final coarsening phase we increase the time step a bit:

# %%
tau.value = 4e-02
fig = pyplot.figure(figsize=(30,10))
count = 0
pos = 1
while t.value < 2.0:
    df_n.assign(df)
    info = scheme.solve(target=df)
    t.value += tau
    count += 1
    if count % 10 == 0:
        df.plot(figure=(fig,140+pos),colorbar=None,clim=[-1,1])
        energy = integrate(polyGrid,Eint(df),order=5)
        print("[",pos,"]",t.value,tau.value,energy,info,flush=True)
        pos += 1
