#! /bin/bash
set -e
set -u
set -- --opts="/duneci/dune.opts" "${@}"
DUNECONTROL=dunecontrol

# export PETSC_DIR=/usr/lib/petsc # petsc4py doesn't build with version available in docker container

pip install -i https://gitlab.dune-project.org/api/v4/projects/812/packages/pypi/simple --no-build-isolation wheel
pip install -i https://gitlab.dune-project.org/api/v4/projects/812/packages/pypi/simple --no-build-isolation --upgrade Pygments
pip install -i https://gitlab.dune-project.org/api/v4/projects/812/packages/pypi/simple --no-build-isolation -r reqCI.txt
# check including portalocker
# pip install -i https://gitlab.dune-project.org/api/v4/projects/812/packages/pypi/simple --no-build-isolation portalocker

python -m ipykernel install --user --name=dune-env
jupyter kernelspec list

cd /duneci/modules
./dune-common/bin/setup-dunepy.py
cd $CI_PROJECT_DIR

echo "*******************************"
pip list
which pandoc
echo "*******************************"

parallel_opts=
if [[ -v DUNECI_PARALLEL ]]; then
  echo "Parallel run with ${DUNECI_PARALLEL} processes"
  parallel_opts="-j${DUNECI_PARALLEL}"
fi
export OMPI_MCA_rmaps_base_oversubscribe=1
export OMPI_MCA_mpi_yield_when_idle=1
export OMPI_MCA_btl_base_warn_component_unused=0
set -x

duneci-standard-test

export DUNE_LOG_LEVEL=DEBUG
ret=0
cd doc
if [[ $REBUILD == "on" ]]; then
  make clean
  make -ki ${parallel_opts}
  makeResult=`make -n`
  if [ -z "$makeResult" ]; then
    ret=1
  fi
else
  touch concepts.py
  make concepts_nb.ipynb
  ret="$?"
fi
cd ..

${DUNECONTROL} --current make doc

if [[ $REBUILD == "on" ]]; then
  tar cvzf doc.tar.gz --dereference doc
  curl --header "JOB-TOKEN: $CI_JOB_TOKEN" --upload-file $CI_PROJECT_DIR/doc.tar.gz $REGURL/tutorials/0.0.1/tutorial.tar.gz
fi

exit "$ret"
