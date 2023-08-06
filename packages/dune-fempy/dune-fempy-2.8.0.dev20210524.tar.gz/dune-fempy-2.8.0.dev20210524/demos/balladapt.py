# %% [markdown]
# # Re-entrant Corner Problem
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
import numpy as np
import matplotlib.pyplot as pyplot
from dune.fem.plotting import plotPointData as plot
import dune.grid as grid
from dune.grid import cartesianDomain, Marker
import dune.fem as fem
from dune.fem.view import adaptiveLeafGridView as adaptiveGridView
from dune.fem.space import lagrange as lagSpace
from dune.fem.space import dgonb as dgSpace
from dune.alugrid import aluConformGrid as leafGridView
from dune.fem.function import integrate, uflFunction
from ufl import *
from dune.ufl import DirichletBC


# use a second order space
order = 2

# set the angle for the corner (0<angle<=360)
cornerAngle = 320.


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
domain = cartesianDomain([0,0], [1,1], [8,8])
gridView = adaptiveGridView( leafGridView(domain) )
gridView.hierarchicalGrid.globalRefine(2)
space = lagSpace(gridView, order=order, storage="istl")
dgspc = dgSpace(gridView, order=order, storage='fem')

x = SpatialCoordinate(space.cell())

# exact solution for this angle
Phi = cornerAngle / 180 * pi
phi = atan_2(x[1], x[0]) + conditional(x[1] < 0, 2*pi, 0)
exact = -sin(pi*x[0])*sin(6*pi*x[1])

def markh(t,element):
    y = element.geometry.center
    y[ 0 ] -= 0.5 + 0.2*np.cos( t );
    y[ 1 ] -= 0.5 + 0.2*np.sin( t );
    if np.dot(y,y) < 0.01:
        return Marker.refine if element.level < 6 else Marker.coarsen

    return Marker.coarsen



t = 0.0
gridView.hierarchicalGrid.mark(lambda e: markh(t,e))
fem.adapt(gridView.hierarchicalGrid)

vh = space.interpolate( exact, name='vh')
uh = dgspc.interpolate( exact, name='uh')

vtk = gridView.sequencedVTK("balladapt", pointdata=[vh], celldata=[uh])
vtk()

while t < 1.0:
    gridView.hierarchicalGrid.mark(lambda e: markh(t,e))
    #gridView.hierarchicalGrid.mark(markh)
    fem.adapt([vh,uh])
    fem.loadBalance([vh,uh])
    vtk()

    if gridView.comm.rank == 0:
        print(f"t = {t}, grid = {gridView.size(0)}")
    t += 0.025
