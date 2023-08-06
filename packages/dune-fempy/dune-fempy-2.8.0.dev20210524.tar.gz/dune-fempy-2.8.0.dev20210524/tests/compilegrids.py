import sys
import time
from dune.grid import structuredGrid, cartesianDomain
from dune.fem.view import adaptiveLeafGridView as gridView

dim = sys.argv[1]

if dim == "2":
    # 2d structured grid
    grid = structuredGrid([0, 0], [1, 1], [4, 4])

    try:
        from dune.alugrid import aluConformGrid, aluSimplexGrid, aluCubeGrid
        domain = cartesianDomain( [0, 0], [1, 1], [4, 4] )

        # 2d alu conform grid
        grid = gridView( aluConformGrid( domain ) )
        # 2d alu simplex grid
        grid = gridView( aluSimplexGrid( domain ) )
        # 2d alu cube grid
        grid = gridView( aluCubeGrid( domain ) )
    except ImportError:
        print("Cannot import module dune-alugrid, skipping grid creation!")

elif dim == "3":
    # 3d structured grid
    grid = structuredGrid([0, 0, 0], [1, 1, 1], [4, 4, 4])

    try:
        from dune.alugrid import aluConformGrid, aluSimplexGrid, aluCubeGrid
        domain = cartesianDomain( [0, 0, 0], [1, 1, 1], [4, 4, 4] )

        # 3d alu conform grid
        grid = gridView( aluConformGrid( domain ) )
        # 3d alu simplex grid
        grid = gridView( aluSimplexGrid( domain ) )
        # 3d alu cube grid
        grid = gridView( aluCubeGrid( domain ) )
    except ImportError:
        print("Cannot import module dune-alugrid, skipping grid creation!")
else:
    print("usage: ",sys.argv[0]," <dimension = 2 or 3>", dim)
