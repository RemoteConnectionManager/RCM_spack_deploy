#!/bin/bash

#current status odf spack PR


export PR_NEEDED="3224" #default to enable autoload
#PR_NEEDED="${PR_NEEDED} 2664" #include 2771 #2771 #add -d option to specify source folder for diy
PR_NEEDED="${PR_NEEDED} 2771" #include 2771 #2771 #add -d option to specify source folder for diy
PR_NEEDED="${PR_NEEDED} 3208" #fix gtkplus build  #### to test

export PR_CLIENT_NEEDED="3057"  #Bootstrap environment modules in setup_env.sh
#PR_CLIENT_NEEDED="${PR_CLIENT_NEEDED} 2548" #concretization of build-only deps separately
export PR_CLUSTER_NEEDED="3250" #fix modulecmd use, needed for parsing module on Marconi and Galileo

export PR_UTILS="" 
PR_UTILS="${PR_UTILS} 2902" #enable including tcl file into modules
PR_UTILS="${PR_UTILS} 3133" #Bundle Packages
#PR_UTILS="${PR_UTILS} 2686" #Command Line config Scopes add---> --config +</path/to/config/dir>
#PR_UTILS="${PR_UTILS} 2694" #Fix some Bugs when Merging Configurations

export PR_TEST=""
#PR_TEST="${PR_TEST} 1167" #register external package in db
#PR_TEST="${PR_TEST} 2507" #simplify add external packages to packages.yaml
PR_TEST="${PR_TEST} 2548" #concretization of build-only deps separately 

export PR_PROD="$PR_NEEDED $PR_CLIENT_NEEDED $PR_CLUSTER_NEEDED $PR_UTILS"
export PR_ALL="$PR_TEST $PR_PROD"

python scripts/deploy_setup.py --integration --clearconfig --debug=debug  --branches clean/develop     pr/.*  wip/.*  --prlist ${PR_PROD} $*


#python scripts/deploy_setup.py --integration --clearconfig --debug=debug  --branches clean/develop     pr/.*  wip/.*  --prlist  2507 2548 2622 2686 2694 2771 2902 2960 2980 3057 3133 3224 3208 3250 $*

#python scripts/deploy_setup.py --integration --clearconfig --debug=debug  --branches clean/develop      --prlist  2507 2548 2622 2686 2694 2771 2902 2960 2980 3057 3133 3224 3208 3250 $*


#2622 openjdk ---- not working----
#2664 #include 2771
#2771 #add -d option to specify source folder for diy

#2980 #fix intel compiler spack install petsc+mpi%intel ^intel-parallel-studio #### conflicts







