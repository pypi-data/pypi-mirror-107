#!/bin/bash

#
# This script builds a Python package index on gitlab.dune-project.org. Such an
# index is necessary as a drop-in replacement for PyPI in continuous integration,
# when runners operate with restricted network access.
#

# This script exits upon errors
set -e

# Create a temporary directory as workspace for this script
TMPDIR=$(mktemp -d)
pushd $TMPDIR

python3 -m venv env
source env/bin/activate
python -m pip install pip-download twine

# pip-download -d $(pwd)/downloads \
#  dune-common \
#  dune-geometry \
#  dune-grid \
#  dune-alugrid \
#  dune-istl \
#  dune-localfunctions \
#  dune-fem \
#  dune-vem \
#  dune-fem-dg

# pip-download -d $(pwd)/downloads \
#  pyparsing \
#  mpi4py

# pip-download -d $(pwd)/downloads \
#  Pygments==2.7.3 \
#  jupyterlab-pygments==0.1.2 \
#  fenics-ufl

# pip-download -d $(pwd)/downloads \
#   apidoc\
#   gmsh\
#   ipython\
#   jinja2\
#   jupyter\
#   mayavi\
#   nbsphinx\
#   matplotlib\
 #  jupytext\
#   pandas\
#   pandoc\
#   pygmsh\
#   pyqt5\
#   sparkmonitor\
#   sphinx-autobuild\
#   sphinx_rtd_theme\
#   sphinxcontrib-bibtex\
#   sortedcontainers\
#   triangle\
#   wheel\
#   x3d\
#   petsc4py

pip-download -d $(pwd)/downloads gmsh
# Upload the packages to the index
for filename in downloads/*
do
  python -m twine upload --verbose --repository gitlab $filename
  echo upload $filename
done

# Clean up the temporary directory
popd
rm -rf $TMPDIR
