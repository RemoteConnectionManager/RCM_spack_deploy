#!/bin/bash

python scripts/deploy_setup.py --integration --dest=deploy/spack1 --debug=debug  --branches clean/develop     pr/.*  wip/.*  --prlist 1167 2622 2686 2694 2771 2902 2960 2980 3057 3133 3224 3250 $*


#1167 register external package in db
#2622 openjdk
#2686 #Command Line config Scopes add---> --config +</path/to/config/dir>
#2694 #Fix some Bugs when Merging Configurations
#2771 #add -d option to specify source folder for diy
#2902 #enable including tcl file into modules
#2980 #fix intel compiler spack install petsc+mpi%intel ^intel-parallel-studio
#3057 #Bootstrap environment modules in setup_env.sh
#3133 #Bundle Packages
#3111 #fix in module parsing

##########  would like to have   #######
#2507 #simplify add external packages to packages.yaml
