#!/bin/bash
# Absolute path to this script. /home/user/bin/foo.sh

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
export RCM_DEPLOY_HOSTPATH=$( cd -P "$( dirname "$SOURCE" )" && pwd )
echo "dir is-->$RCM_DEPLOY_HOSTPATH<--"
source ${RCM_DEPLOY_HOSTPATH}/../../../get_root
export RCM_DEPLOY_SPACKPATH=${RCM_DEPLOY_ROOTPATH}/deploy/spack


${RCM_DEPLOY_ROOTPATH}/spack_config

source ${RCM_DEPLOY_SPACKPATH}/share/spack/setup-env.sh

${RCM_DEPLOY_ROOTPATH}/spack_init

export LOGFILE=${RCM_DEPLOY_HOSTPATH}/build_rcm.$$.log

spack install --verbose py-flake8 >> ${LOGFILE}  2>&1
#spack install --verbose environment-modules >> ${LOGFILE}  2>&1

