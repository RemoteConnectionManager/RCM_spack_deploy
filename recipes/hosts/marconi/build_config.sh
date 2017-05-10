#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file wa
s located
done
export RCM_DEPLOY_HOSTPATH="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
source ${RCM_DEPLOY_HOSTPATH}/../../../setup.sh
export RCM_GIT_PATH=${RCM_DEPLOY_ROOTPATH}/deploy/RCM
echo "HOSTPATH-->${RCM_DEPLOY_HOSTPATH}<--"
echo "ROOTPATH-->${RCM_DEPLOY_ROOTPATH}<--"
echo "DESTPATH-->$(pwd)<--"
echo "GITREPO-->${RCM_GIT_PATH}<--"

export RCM_DEPLOY_COMMAND="python ${RCM_DEPLOY_ROOTPATH}/scripts/deploy_setup.py --integration --clearconfig --debug=debug  --branches clean/develop     pr/.*  wip/.* --prlist $PR_NEEDED $PR_CLUSTER_NEEDED $PR_UTILS --dest $(pwd)/spack  --config ${RCM_DEPLOY_HOSTPATH} --install $(pwd)/install" 

cat ${RCM_DEPLOY_HOSTPATH}/build.job.head > build.job
echo "export LOGFILE=$(pwd)/log_build.\${PBS_JOBID}.log" >> build.job
echo "cd $(pwd)/spack" >> build.job
echo "source share/spack/setup-env.sh" >> build.job
echo "spack install -v --only dependencies rcm@develop+linksource > ${LOGFILE} 2>&1" >> build.job
echo "spack diy --source-path ${RCM_GIT_PATH} rcm@develop+linksource >> ${LOGFILE}  2>&1" >> build.job

#spack install -v --only dependencies rcm@develop+linksource   > ${LOGFILE}  2>&1
#spack diy --source-path ${RCM_GIT_PATH} rcm@develop+linksource >> ${LOGFILE}  2>&1
#spack install -v qt   >> ${LOGFILE}  2>&1
#spack install -v font-adobe-100dpi  >> ${LOGFILE}  2>&1


