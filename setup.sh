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

export PR_NEEDED="3224" #default to enable autoload
#PR_NEEDED="${PR_NEEDED} 2664" #include 2771 #2771 #add -d option to specify source folder for diy
PR_NEEDED="${PR_NEEDED} 2771" #include 2771 #2771 #add -d option to specify source folder for diy
#merged#PR_NEEDED="${PR_NEEDED} 3208" #fix gtkplus build  #### to test

export PR_CLIENT_NEEDED="3057"  #Bootstrap environment modules in setup_env.sh
#unstable#PR_CLIENT_NEEDED="${PR_CLIENT_NEEDED} 2548" #concretization of build-only deps separately
#merged#PR_CLIENT_NEEDED="${PR_CLIENT_NEEDED} 4145" #concretization problems stopgap for py+tk, alternative to 2548
#conflict#export PR_CLUSTER_NEEDED="3250" #fix modulecmd use, needed for parsing module on Marconi and Galileo

export PR_CLIENT_PATCHES="fix/pull/#2548/py-flake8 pull/2548/updated"

export PR_UTILS="" 
PR_UTILS="${PR_UTILS} 2902" #enable including tcl file into modules
#conflict#PR_UTILS="${PR_UTILS} 3133" #Bundle Packages
#PR_UTILS="${PR_UTILS} 2686" #Command Line config Scopes add---> --config +</path/to/config/dir>
#PR_UTILS="${PR_UTILS} 2694" #Fix some Bugs when Merging Configurations

export PR_TEST=""
#merged#PR_TEST="${PR_TEST} 1167" #register external package in db
#PR_TEST="${PR_TEST} 2507" #simplify add external packages to packages.yaml
#PR_TEST="${PR_TEST} 2548" #concretization of build-only deps separately 



