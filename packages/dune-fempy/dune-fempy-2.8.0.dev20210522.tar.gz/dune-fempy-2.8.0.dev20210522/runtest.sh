if [ "$1" == "latest" ] ; then
  DUNEVERSION=""
  dockerName=registry.dune-project.org/dune-fem/dune-fem-dev:latest
elif [ "$1" != "" ] ; then
  DUNEVERSION=$1
  dockerName=registry.dune-project.org/dune-fem/dune-fem-dev:$1
else
  DUNEVERSION=""
  dockerName=registry.dune-project.org/dune-fem/dune-fem-dev:latest
fi

# need to check if docker is called using 'sudo'
if [ ! "$SUDO_UID" = "" ] ;
then
  USERID=$SUDO_UID
  USERNAME=$SUDO_USER
else
  USERID=$(id -u)
  USERNAME=$USER
fi
if [ ! "$SUDO_GID" = "" ] ;
then
  GROUPID=$SUDO_GID
else
  GROUPID=$(id -g)
fi

# now start docker container
xhost +si:localuser:$USERNAME
docker run -it --rm --name dunepy$DUNEVERSION -v $PWD:/host -v dunepy$DUNEVERSION:/dunepy \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro --device /dev/dri \
    -e userId=$USERID -e groupId=$GROUPID --hostname="dunepy" --add-host dunepy:127.0.0.1 $dockerName \
    -c /host//buildTutorial.sh
xhost -si:localuser:$USER

# add test to see if everything worked
cd doc
if make -q
then
  cd ..
  cd build-cmake
  make clean
  rm -rf doc
  cmake .
  make doc
else
  cd ..
  echo "Make failed not building documentation"
  exit 1
fi
