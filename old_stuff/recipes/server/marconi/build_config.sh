#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file wa
s located
done
export RCM_DEPLOY_HOSTPATH="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
#echo "PRIMA----- RCM_DEPLOY_HOSTPATH = ${RCM_DEPLOY_HOSTPATH}  RCM_DEPLOY_SPEC=${RCM_DEPLOY_SPEC}"
source ${RCM_DEPLOY_HOSTPATH}/../setup.sh
#echo "DOPO----- RCM_DEPLOY_SPEC=${RCM_DEPLOY_SPEC}"
#echo "ROOTPATH-->${RCM_DEPLOY_ROOTPATH}<--"
export RCM_DEPLOY_SPEC="${RCM_DEPLOY_SPEC}+mesa"
source ${RCM_DEPLOY_ROOTPATH}/setup_1.sh
export RCM_DEPLOY_BUILD_COMMAND="qsub -v RCM_DEPLOY_BUILD_DEPS,RCM_DEPLOY_SPACK_SETUP_COMMAND ${RCM_DEPLOY_HOSTPATH}/build.job"
echo "RCM_DEPLOY_BUILD_COMMAND -->${RCM_DEPLOY_BUILD_COMMAND}<--"
#echo "HOSTPATH-->${RCM_DEPLOY_HOSTPATH}<--"
#echo "GITREPO-->${RCM_GIT_PATH}<--"
#echo "DESTPATH-->$RCM_DEPLOY_SPACK_PATH<--"



