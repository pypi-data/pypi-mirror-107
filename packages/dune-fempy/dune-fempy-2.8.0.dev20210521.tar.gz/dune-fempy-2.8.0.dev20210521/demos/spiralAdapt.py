import sys
import math
import ufl
from ufl import div, grad, inner, dot, dx, dS, jump, avg, outer
import dune.ufl
import dune.grid
import dune.fem
import dune.alugrid

from dune.grid import cartesianDomain, gridFunction
from dune.fem import parameter

parameter.append({"fem.verboserank": 0})

dim = 2
if len(sys.argv) > 1:
    dim = int(sys.argv[1])
print("Using dim = ",dim)

maxOrder = 1
if len(sys.argv) > 2:
    maxOrder = int(sys.argv[2])
print("Using max-order = ",maxOrder)

# %% [markdown]
# In our attempt we will discretize the model as a 2x2 system. Here are some possible model parameters and initial conditions (we even have two sets of model parameters to choose from):
# %%
nonConforming = False
usePAdapt = False
linearSpiral = True
# maxLevel = 5 for 2d and 4 for 3d
maxLevel     = 5
# startLevel = 2 for 2d and 1 for 3d
startLevel   = 2 # 1 if dim == 3 else 2
dt           = dune.ufl.Constant(0.1,"dt")
t            = dune.ufl.Constant(0,"time")
endTime      = 15.
saveInterval = 1.0
maxTol       = 1e-4

if linearSpiral:
    spiral_a   = 0.75
    spiral_b   = 0.02
    spiral_eps = 0.02
    spiral_D   = 1./100
    def spiral_h(u,v): return u - v
else:
    spiral_a   = 0.75
    spiral_b   = 0.0006
    spiral_eps = 0.08
    def spiral_h(u,v): return u**3 - v


# %% [markdown]
# Now we set up the reference domain, the Lagrange finite element space (second order), and discrete functions for $(u^n,v^n($, $(u^{n+1},v^{n+1})$:
# %%
if dim == 3:
    domain   = dune.grid.cartesianDomain([0,0,0],[2.5,2.5,2.5],[5,5,5])
else:
    domain   = dune.grid.cartesianDomain([0,0],[2.5,2.5],[5,5])

if nonConforming:
    baseView = dune.alugrid.aluCubeGrid(domain)
    #baseView = dune.alugrid.aluSimplexGrid("spiral.dgf", dimgrid=dim, dimworld=dim)
    #baseView = dune.alugrid.aluSimplexGrid(domain)
else:
    baseView = dune.alugrid.aluConformGrid(domain)
    #baseView = dune.grid.ugGrid("unit.dgf", dimgrid=dim, worlddim=dim)

gridView = dune.fem.view.adaptiveLeafGridView( baseView )

print("Initial grid: n-element = ",gridView.size( 0 ))

maxLevel *= gridView.hierarchicalGrid.refineStepsForHalf
startLevel *= gridView.hierarchicalGrid.refineStepsForHalf
gridView.hierarchicalGrid.globalRefine(startLevel)

if nonConforming:
    space = dune.fem.space.lagrangehp( gridView, order=maxOrder, storage="istl" )
else:
    space = dune.fem.space.lagrange( gridView, order=maxOrder, storage="istl" )

x = ufl.SpatialCoordinate(space)
iu = lambda s: ufl.conditional(s > 1.25, 1, 0 )
top = 1.0
if dim == 3:
    top = ufl.conditional( x[2] > 1.25,1,0)

initial_u = iu(x[1])*top + iu(2.5-x[1])*(1.0 - top)
#initial_u = ufl.conditional( x[2] > 1.25, iu(x[1]), iu(2.5 - x[1]))
initial_v = ufl.conditional(x[0]<1.25,0.5,0)

uh     = space.interpolate( initial_u, name="u" )
if usePAdapt:
    maxOrderpm1 = maxOrder-1 if maxOrder > 1 else maxOrder
    spcpm = dune.fem.space.lagrangehp( gridView, order=maxOrderpm1, storage="istl" )
    uh_pm1 = spcpm.interpolate( initial_u, name="u_p-1" )
uh_n = uh.copy()
vh   = space.interpolate( initial_v, name="v" )
vh_n = vh.copy()


# %% [markdown]
# Setting up the model
# %%
u   = ufl.TrialFunction(space)
phi = ufl.TestFunction(space)
hT  = ufl.MaxCellEdgeLength(space.cell())
hS  = ufl.avg( ufl.MaxFacetEdgeLength(space.cell()) )
hs =  ufl.MaxFacetEdgeLength(space.cell())('+')
n   = ufl.FacetNormal(space.cell())
penalty = 5 * (maxOrder * ( maxOrder + 1 )) * spiral_D

ustar          = lambda v: (v+spiral_b)/spiral_a
diffusiveFlux  = lambda w,d: spiral_D * d
source         = lambda u1,u2,u3,v: -1/spiral_eps * u1*(1-u2)*(u3-ustar(v))
source         = lambda u1,u2,u3,v: -1/spiral_eps * u1*(1-u2)*(u3-ustar(v))

# main terms
xForm  = inner(diffusiveFlux(u,grad(u)), grad(phi)) * dx
xForm += ufl.conditional(uh_n<ustar(vh_n), source(u,uh_n,uh_n,vh_n), source(uh_n,u,uh_n,vh_n)) * phi * dx
# dg terms
if nonConforming:
    xForm -= ( inner( outer(jump(u), n('+')), avg(diffusiveFlux(u,grad(phi)))) +\
               inner( avg(diffusiveFlux(u,grad(u))), outer(jump(phi), n('+'))) ) * dS
    xForm += penalty/hS * inner(jump(u), jump(phi)) * dS
# adding time discretization
form   = ( inner(u,phi) - inner(uh_n, phi) ) * dx + dt*xForm

equation   = form == 0

def markp(element):
    return 2

# initial mark
if usePAdapt:
    dune.fem.spaceAdapt(space,markp,[uh])

def markpm1(element):
    return space.localOrder( element ) - 1


# %% [markdown]
# The model is now completely implemented and can be created, together with the corresponding scheme:
# %%
solverParameters =\
       {"newton.tolerance": 1e-8,
        "newton.linear.tolerance": 1e-12,
        "newton.linear.preconditioning.method": "amg-ilu",
        "newton.linear.maxiterations":1000,
        "newton.verbose": False,
        "newton.linear.verbose": True}
scheme = dune.fem.scheme.galerkin( equation, solver="gmres", parameters=solverParameters)

# %% [markdown]
# Error estimator
# %%
fvspace = dune.fem.space.finiteVolume(uh.space.grid)
estimate = fvspace.interpolate([0], name="estimate")
estimate_pm1 = fvspace.interpolate([0], name="estimate_pm1")

chi = ufl.TestFunction(fvspace)

residual = (u-uh_n)/dt - div(diffusiveFlux(u,grad(u))) + source(u,u,u,vh)

estimator_ufl = hT**2 * residual**2 * chi * dx +\
                hS * inner( jump(diffusiveFlux(u,grad(u))), n('+'))**2 * avg(chi) * dS +\
                1/hS * jump(u)**2 * avg(chi) * dS
estimator = dune.fem.operator.galerkin(estimator_ufl)

# %% [markdown]
# Time loop
# %%
@gridFunction(gridView,"pDegree")
def pDegree(element,x):
    return space.localOrder(element)

nextSaveTime = saveInterval
count = 0
levelFunction = dune.fem.function.levelFunction(gridView)
subSampling = 1 if maxOrder < 3 else 2
gridView.writeVTK("spiral", pointdata=[uh,vh], number=count, celldata=[estimate,levelFunction,pDegree], subsampling=subSampling)
gridView.writeVTK("spiral-grid", pointdata=[uh,vh], number=count, celldata=[estimate,levelFunction,pDegree])
count += 1

@gridFunction(gridView,name="pEstimate")
def pEstimator(e,x):
    r    = estimate.localFunction(e).evaluate(x)
    r_p1 = estimate_pm1.localFunction(e).evaluate(x)
    # if r[0] < 1e-15:
    #     eta = 0
    # else:
    #     eta = abs(r[0]-r_p1[0]) / r[0]
    eta = abs(sum(r)-sum(r_p1))
    return [eta, sum(r), sum(r_p1)]

def markpDiff(element):
    # ptol = 1e-5    # for relative
    ptol = 1e-10 # 1e-17   # absolute
    # evaluate smoothness indicator
    eta = pEstimator(element,element.referenceElement.center)
    # get current polorder
    polorder = space.localOrder(element)

    newPolorder = polorder
    if eta[0] < ptol:
        newPolorder = polorder-1 if polorder > 1 else polorder
    elif eta[0] > 100.*ptol:
        newPolorder = polorder+1 if polorder < maxOrder else polorder

    return newPolorder

while t.value < endTime:
    uh_n.assign(uh)
    vh_n.assign(vh)
    info = scheme.solve(target=uh)
    t.value += dt.value
    print("Computed solution at time", t.value,
          "iterations: ", info["linear_iterations"],
          "#Ent: ", gridView.size(0) )
    vh.interpolate( vh_n + dt*spiral_h(uh_n, vh_n) )

    estimator(uh, estimate)
    maxEst = max(estimate.dofVector)
    print("max est: ", maxEst)
    if t.value >= nextSaveTime-0.01 or t.value >= endTime:
        print("Writing vtu at time ", t.value," count = ", count )
        gridView.writeVTK("spiral", pointdata=[uh,vh], number=count, subsampling=subSampling)
        gridView.writeVTK("spiral-grid", pointdata=[uh,vh], number=count, celldata=[levelFunction,pDegree])
        nextSaveTime = t.value + saveInterval
        count += 1
    if t.value > 5:
        dune.fem.mark(estimate, maxTol, 0.05 * maxTol, 0,maxLevel)
        dune.fem.adapt([uh,vh])
        if usePAdapt:
            # mark space with one p lower locally
            dune.fem.spaceAdapt(spcpm,markpm1,[uh_pm1])
            uh_pm1.interpolate( uh )
            estimator(uh_pm1, estimate_pm1)
            estimator(uh, estimate)
            dune.fem.spaceAdapt(space,markpDiff, [uh])
        else:
            print("P-Adaptation is disabled!")
