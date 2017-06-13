#! /bin/bash
# Absolute path to this script. /home/user/bin/foo.sh

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file wa
s located
done
export RCM_DEPLOY_ROOTPATH="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
export RCM_GIT_PATH=${RCM_DEPLOY_ROOTPATH}/deploy/RCM

export RCM_DEPLOY_SPACK_PATH=$(pwd)/$1
export RCM_DEPLOY_SPACK_SETUP_COMMAND="source ${RCM_DEPLOY_SPACK_PATH}/share/spack/setup-env.sh"
export RCM_DEPLOY_INSTALL_PATH=$(pwd)/install

export RCM_DEPLOY_PR_NEEDED="3224" #default to enable autoload
#PR_NEEDED="${PR_NEEDED} 2664" #include 2771 #2771 #add -d option to specify source folder for diy
RCM_DEPLOY_PR_NEEDED="${RCM_DEPLOY_PR_NEEDED} 2771" #include 2771 #2771 #add -d option to specify source folder for diy
#merged#PR_NEEDED="${PR_NEEDED} 3208" #fix gtkplus build  #### to test


export RCM_DEPLOY_PR_UTILS="" 
RCM_DEPLOY_PR_UTILS="${RCM_DEPLOY_PR_UTILS} 2902" #enable including tcl file into modules
#conflict#PR_UTILS="${PR_UTILS} 3133" #Bundle Packages
#PR_UTILS="${PR_UTILS} 2686" #Command Line config Scopes add---> --config +</path/to/config/dir>
#PR_UTILS="${PR_UTILS} 2694" #Fix some Bugs when Merging Configurations

export RCM_DEPLOY_PR_TEST=""
#merged#PR_TEST="${PR_TEST} 1167" #register external package in db
#PR_TEST="${PR_TEST} 2507" #simplify add external packages to packages.yaml
#PR_TEST="${PR_TEST} 2548" #concretization of build-only deps separately 

export RCM_DEPLOY_SPEC="rcm@develop+linksource"



