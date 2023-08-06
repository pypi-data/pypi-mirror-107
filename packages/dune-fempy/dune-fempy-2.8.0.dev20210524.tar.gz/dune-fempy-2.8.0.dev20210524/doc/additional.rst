.. _scripts:

#####################
Notebooks and Scripts
#####################

All examples (both as scripts and notebooks) as well as grid files etc
are available in the `demo` folder of the git repository
https://gitlab.dune-project.org/dune-fem/dune-fempy
or can be downloaded here:

================================================= ================================================= =================================================
Example                                           Notebooks                                         Scripts
================================================= ================================================= =================================================
General Concepts                                  :download:`notebook <concepts_nb.ipynb>`          :download:`script <concepts.py>`
Time Dependent Problem                            :download:`notebook <dune-fempy_nb.ipynb>`        :download:`script <dune-fempy.py>`
Using different linear solver packages            :download:`notebook
<solvers_nb.ipynb>` :download:`script <solvers.py>`
boundary_nb.ipynb
discontinuousgalerkin_nb.ipynb
othergrids_nb.ipynb
backuprestore_nb.ipynb

Full Grid Interface                               :download:`notebook <dune-corepy_nb.ipynb>`       :download:`script <dune-corepy.py>`
Bending beam (linear elasticity)                  :download:`notebook <elasticity_nb.ipynb>`        :download:`script <elasticity.py>`
Spiral wave (reaction diffusion system)           :download:`notebook <spiral_nb.ipynb>`            :download:`script <spiral.py>`
Slit domain (wave equation)                       :download:`notebook <wave_nb.ipynb>`              :download:`script <wave.py>`
Saddle point solver (stokes flow)                 :download:`notebook <uzawa-scipy_nb.ipynb>`       :download:`script <uzawa-scipy.py>`
Adaptive FE (laplace problem)                     :download:`notebook <laplace-adaptive_nb.ipynb>`  :download:`script <laplace-adaptive.py>`
Adaptive FE (using DWR)                           :download:`notebook <laplace-dwr_nb.ipynb>`       :download:`script <laplace-dwr.py>`
Crystal growth (phase field model)                :download:`notebook <crystal_nb.ipynb>`           :download:`script <crystal.py>`
Time dependent surface (mean curvature flow)      :download:`notebook <mcf_nb.ipynb>`               :download:`script <mcf.py>`
chemical_nb.ipynb euler_nb.ipynb
HP adaptive DG (two phase flow)                   :download:`notebook <twophaseflow_nb.ipynb>`      :download:`script <twophaseflow.py>`
Virtual element method                            :download:`notebook <vemdemo_nb.ipynb>`           :download:`script <vemdemo.py>`
chimpl_nb.ipynb
================================================= ================================================= =================================================



###############################
Mesh Files used in the Examples
###############################

:download:`unit cube grid file <unitcube-2d.dgf>`
:download:`sphere grid file <sphere.dgf>`
:download:`three quarters sphere grid with boundary <soap.dgf>`
:download:`slit domain mesh <wave_tank.msh>`
 
###################
Citing this project
###################

If you found this tutorial helpful for getting your own projects up and
running please cite this project:

Title: Python Bindings for the DUNE-FEM module
*Authors: Andreas Dedner, Martin Nolte, and Robert Klöfkorn*
Publisher: Zenodoo, 2020
DOI 10.5281/zenodo.3706994

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3706994.svg
   :target: https://doi.org/10.5281/zenodo.3706994

#################################
List of things that need doing...
#################################

.. todolist::


