.. sectionauthor:: Andreas Dedner <a.s.dedner@warwick.ac.uk>, Robert Kl\ |oe|\ fkorn <robert.kloefkorn@iris.no>, Martin Nolte <nolte.mrtn@gmail.com>

.. _algorithms:

#######################
Using C++ Code Snippets
#######################

.. todo:: link to `developers.rst`

In this section we demonstrate how it possible to use small piece of C++
code to either extend the existing functionality or improve the efficiency
of the code by moving code from Python to C++.  We have already seen how to
define grid functions using C++ code snippets in the
:ref:`Grid Function</concepts_nb.ipynb#Grid-Functions>` section
In the following we will move parts of an algorithm from
Python to C++. The DUNE interfaces exported to
Python are very close to their C++ counterpart so that rapid prototyping of
new algorithms can be carried out using Python and then easily moved to
C++. This will be demonstrated in the following examples:

.. toctree::
   :maxdepth: 2

   mcf-algorithm_nb
   laplace-dwr_nb
   lineplot_nb
