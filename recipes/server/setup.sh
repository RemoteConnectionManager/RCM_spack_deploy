#! /bin/bash
# Absolute path to this script. /home/user/bin/foo.sh

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file wa
s located
done
source $( cd -P "$( dirname "$SOURCE" )" && pwd )/../../setup.sh	
export RCM_DEPLOY_MASTER_BRANCH=integrate/server
export RCM_DEPLOY_PRLIST="$RCM_DEPLOY_PR_NEEDED $RCM_DEPLOY_PR_UTILS $RCM_DEPLOY_PR_TEST"
export RCM_DEPLOY_SPEC="${RCM_DEPLOY_SPEC}+server"




