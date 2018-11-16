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

export RCM_DEPLOY_PR_CLIENT_NEEDED="3057"  #Bootstrap environment modules in setup_env.sh
#unstable#PR_CLIENT_NEEDED="${PR_CLIENT_NEEDED} 2548" #concretization of build-only deps separately
#merged#PR_CLIENT_NEEDED="${PR_CLIENT_NEEDED} 4145" #concretization problems stopgap for py+tk, alternative to 2548
#conflict#export PR_CLUSTER_NEEDED="3250" #fix modulecmd use, needed for parsing module on Marconi and Galileo


