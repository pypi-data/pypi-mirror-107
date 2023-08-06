SHELL := /bin/bash
PATH := bin:$(PATH)

FIGURES = figures/3dexample.png figures/interpolation_discrete.png figures/interpolation_exact.png figures/interpolation_error.png
NBS = spiral_nb.ipynb uzawa-scipy_nb.ipynb elasticity_nb.ipynb wave_nb.ipynb \
      laplace-adaptive_nb.ipynb crystal_nb.ipynb \
			mcf_nb.ipynb boundary_nb.ipynb solvers_nb.ipynb \
			mcf-algorithm_nb.ipynb lineplot_nb.ipynb laplace-dwr_nb.ipynb othergrids_nb.ipynb \
			concepts_nb.ipynb dune-fempy_nb.ipynb backuprestore_nb.ipynb \
      dune-corepy_nb.ipynb discontinuousgalerkin_nb.ipynb \
      twophaseflow_nb.ipynb euler_nb.ipynb chemical_nb.ipynb \
			geoview_nb.ipynb geoview_nb.rst \
			levelgridview_nb.ipynb levelgridview_nb.rst \
      filteredgridview_nb.ipynb filteredgridview_nb.rst \
      vemdemo_nb.ipynb chimpl_nb.ipynb
			# spiral_adapt_nb.ipynb

# .EXPORT_ALL_VARIABLES:

export DUNE_LOG_LEVEL=WARNING

all: $(NBS) $(FIGURES)

.PHONY: clean distclean linkcheck

linkcheck:
	@sphinx-build -b linkcheck . html

clean:
	@rm -f *.vtu *.pvtu *.p *.png $(FIGURES) $(NBS)
	@rm -f geoview_nb_files/geoview_nb_1_0.png
distclean: clean
	@rm -f *.bbl
	@rm -rf html

.SECONDARY:

%_nb.ipynb: %.py
	@jupytext $< --execute --set-kernel python3 --output $*_nb.ipynb

%_nb.rst: %_nb.ipynb
	@jupyter-nbconvert $< --to rst

figures/3dexample.png: 3dexample.py dune-fempy_nb.ipynb
	@pvpython 3dexample.py

figures/interpolation_discrete.png figures/interpolation_exact.png figures/interpolation_error.png &: interpolation.py dune-corepy_nb.ipynb
	@pvpython interpolation.py
