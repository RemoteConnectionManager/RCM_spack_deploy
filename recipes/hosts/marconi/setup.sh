#!/bin/bash


SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
# resolve $SOURCE until the file is no longer a symli nk
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" 
# if $SOURCE was a relative symli nk, 
# we need to resolve it relative to the path where the symlink file was located
done
export RCM_DEPLOY_HOSTPATH="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
source ${RCM_DEPLOY_HOSTPATH}/../../../get_root
export CONFIG_DIRS="config config/shared_install config/rcm config/rcm/server config/rcm/server/headless config/insitu "
echo "-->$CONFIG_DIRS<--"
if [ "x$1" != "x" ]
then
  RCM_DEPLOY_CURRENT_PATH=deploy/insitu/$1/spack
  if [ "$1" == "dev" ]
  then
    export CONFIG_DIRS="$CONFIG_DIRS config/rcm/develop" 
  fi  
  if [ "$1" == "dev_all" ]
  then
    export CONFIG_DIRS="$CONFIG_DIRS config/openmpi_scheduler config/openfoam config/meteo config/rstudio config/rcm/develop"
  fi  

  if [ "$1" == "dev_all_qt5" ]
  then
    export CONFIG_DIRS="$CONFIG_DIRS config/openmpi_scheduler config/openfoam config/meteo config/rstudio config/rcm/develop"
  fi  

python ${RCM_DEPLOY_ROOTPATH}/scripts/config.py -c $CONFIG_DIRS  --platformconfig --runconfig --dest ${RCM_DEPLOY_CURRENT_PATH}
source ${RCM_DEPLOY_ROOTPATH}/${RCM_DEPLOY_CURRENT_PATH}/share/spack/setup-env.sh
else
  echo "Please specify deployment name folder like:"
  echo "$0 dev"
fi
