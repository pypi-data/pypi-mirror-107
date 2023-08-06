.. dune-fem python documentation master file, created by
   Andreas Dedner on Mon Mai 20 2019.

################################
Welcome to the dune-fem tutorial
################################

This module brings python scripting support to `Dune`_.
This version describes the bindings for the development version
(to become 2.8). It serves three purposes:

1. High level program control for solving partial differential equations
   using classes from the `Dune`_ core and from `Dune-Fem`_
   :cite:`Dune-Grid-Paper,Dune-Fem-Paper`.
   The unified form language `UFL`_ :cite:`UFL-Paper`
   is used to describe the mathematical
   model, all realizations of the `Dune`_ grid interface can be used to
   work with the domain tessellation, and the finite element spaces,
   operator, and solvers provided by `Dune-Fem`_ for the descritizations
   and solving steps. All of this is available within to be used in python
   scripts or through Jupyter notebooks.
2. Rapid prototyping of new methods or other parts of a simulation is easy
   since the interfaces provided are very similar to the `Dune`_ C++
   interface. This makes it easy to transfer a working prototype from
   python (easy to develop) to C++ (high efficiency). Small C++ code
   snippets can be easy called from python using just in time compilation.
3. Rapid prototyping of new implementations of `Dune`_ interfaces. So
   new implementations of the `Dune`_ grid interface can be easily
   tested. For `Dune-Fem`_ developers, new grid views, discrete function spaces, and
   scheme classes following the *Dune-Fem-Howto* concept can be added and tested.

############################
An Overview of this Document
############################

This document tries to describe the main concepts needed to get a new user
started on solving complex partial differential equations using the
`Dune-Fem`_ python bindings. Some parts are still quite raw and we would
greatly appreciate any help improving this document. In addition if you
would like to promote your own work then please upload a script showcasing
some simulation you did bases on this package - it is possibly as easy as
providing us with a Python script. More details on how to help
us improve and extend this document see the section on :ref:`contributing`.

The Python bindings are based on `pybind11`_ :cite:`Pybind11-Paper` and a detailed
description on how we export the polymorphic interfaces in `Dune`_ is
provided in :cite:`Dune-Python-Paper` which describes the dune module
`Dune-Python`_ which after the Dune 2.7 release has been directly
integrated into the Dune core modules. If you have a version newer then 2.8
then note that the `Dune-Python_` module is obsolete.

Here is a quick summary of the different parts of this document - all of
the code is available for download in form of both :ref:`scripts`.
Or can be obtained by cloning the git repository
https://gitlab.dune-project.org/dune-fem/dune-fempy
where they can be found in the demo folder.

#. First off some remarks on getting the package to work: the simplest
   approach is to use the Python package index (pip) to install the software
   into a new virtual environment.
   Docker and working from the git sources is also discussed.
#. A scalar Laplace problem and a simple scalar, non linear time dependent partial
   differential equation
   is used to describe the basic concepts. This leads through the steps
   required to set up the problem, solve the system of equations, and
   visualize the results.
#. After the introduction to the underlying concepts and how to get a
   simple problem up and running, we discuss:

   * how to use different solver backends (including build in solvers, solvers and
     preconditioners available in `Dune-Istl`_, `scipy`_, `petsc`_ and
     also `petsc4py`_ see also :cite:`PETSc-Paper,SciPy-Paper`).
   * how to add more complicated boundary conditions to the problem formulation.
   * how to backup and restore data including discrete functions and the
     grid hierarchy as is useful for example to checkpoint a simulation.
   * more details on constructing a grid using different formats including for
     example `gmsh`_ but also using simple python structures like
     dictionaries for describing general unstructured grids is available.
     Results can be plotted using `matplotlib`_ (for 2d) and for example
     `mayavi`_ (for 2d and 3d). For more advanced plotting options data can
     be exported using `vtk` format and then analysed for example using
     `paraview`_. All of this is demonstrated in the provided examples.
   * discuss the grid interface in more details, i.e., how to iterate over
     the grid, access geometrical information, and attach data to elements
     of the grid.
#. Building upon the general concepts described in the first part, we
   provide scripts showing how to solve far more complex PDEs.
   The :ref:`scripts`
   used for each of these and the following examples can be downloaded
   and are hopefully useful as starting point for new projects.
#. We then discuss some further topics:

   * Local grid refinement and coarsening is a central feature of
     `Dune-Fem`_. Here we show how to use it for stationary and
     time dependent problems. Grid adaptivity makes use of special grid views.i
   * Other views are also
     available, one of these can be used to deform the grid given an
     arbitrary (discrete) vector field. This is used to compute the evolution
     of a surface under mean curvature flow.
   * We complete our discussion by demonstrating how to straightforwardly
     extend the functionality of the package and
     improve performance by important additional C++ algorithms and classes.
#. Finally other projects are presented some of them developed by
   the authors of this document, some contributed by other
   users. If you have used this package then we would like to
   hear about it and would ask you to contribute to this
   chapter. Doing so is quite easy (see :ref:`contributing` for details).

.. _mayavi: https://docs.enthought.com/mayavi/mayavi
.. _paraview: https://www.paraview.org
.. _matplotlib: https://matplotlib.org
.. _gmsh: https://pypi.org/project/pygmsh
.. _scipy: https://www.scipy.org
.. _petsc: https://www.mcs.anl.gov/petsc
.. _petsc4py: https://bitbucket.org/petsc/petsc4py
.. _docker: https://www.docker.com
.. _pybind11: https://github.com/pybind/pybind11
.. _Dune: https://www.dune-project.org
.. _Dune-Istl: https://www.dune-project.org/modules/dune-istl/
.. _Dune-Fem: https://www.dune-project.org/modules/dune-fem/
.. _Dune-Python: https://www.dune-project.org/modules/dune-python/
.. _UFL: https://bitbucket.org/fenics-project/ufl
.. _tutorial compatible with the 2.7 release: https://dune-project.org/sphinx/content/sphinx/dune-fem-2.7/

.. todo:: add more citations



.. toctree::
   :maxdepth: 2
   :caption: Installation

   installation

.. toctree::
   :maxdepth: 3
   :caption: Getting Started

   concepts_nb
   dune-fempy_nb

.. toctree::
   :maxdepth: 2
   :caption: Next Steps

   solvers_nb
   boundary_nb
   othergrids_nb
   backuprestore_nb
   corepy

.. toctree::
   :maxdepth: 2
   :caption: Further Examples

   furtherexamples

.. toctree::
   :maxdepth: 3
   :caption: Further Topics

   gridviews
   cpp
   femdg

.. toctree::
   :maxdepth: 1
   :caption: User Projects
   :name: userprojects

   twophaseflow_descr
   vemdemo_descr

.. toctree::
   :maxdepth: 2
   :caption: Information and Resources

   developers
   contributions
   additional


.. API reference <api/modules>


##################
Indices and Tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

############
Bibliography
############

.. bibliography:: dune-fempy.bib
   :all:
