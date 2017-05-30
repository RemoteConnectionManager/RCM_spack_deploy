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
echo "ROOTPATH-->${RCM_DEPLOY_ROOTPATH}<--"
echo "HOSTPATH-->${RCM_DEPLOY_HOSTPATH}<--"
echo "GITREPO-->${RCM_GIT_PATH}<--"
echo "DESTPATH-->$(pwd)<--"

export RCM_DEVEL_DEPLOY_COMMAND="python ${RCM_DEPLOY_ROOTPATH}/scripts/deploy_setup.py --integration --clearconfig --debug=debug  --master integrate/client --branches clean/develop     pr/.*  wip/.* --prlist $PR_NEEDED $PR_CLIENT_NEEDED $PR_UTILS --dest $(pwd)/spack_devel  --config ${RCM_DEPLOY_HOSTPATH} --install $(pwd)/install" 

export RCM_DEPLOY_COMMAND="python ${RCM_DEPLOY_ROOTPATH}/scripts/deploy_setup.py  --clearconfig --debug=debug  --master integrate/client --branches integrate/client --dest $(pwd)/spack_test  --config ${RCM_DEPLOY_HOSTPATH} --install $(pwd)/install" 

#spack install -v --only dependencies rcm@develop+linksource   > ${LOGFILE}  2>&1
#spack diy --source-path ${RCM_GIT_PATH} rcm@develop+linksource >> ${LOGFILE}  2>&1
#spack install -v qt   >> ${LOGFILE}  2>&1
#spack install -v font-adobe-100dpi  >> ${LOGFILE}  2>&1


