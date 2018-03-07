#!/usr/bin/env bash
#spack repo add @{RCM_DEPLOY_ROOTPATH}/repo --scope site
#spack  compiler find --scope site
#spack info rcm
#spack install --verbose py-flake8
#spack find
#spack module  rm -y
#spack module refresh -y
spack find -l curl
spack spec -l curl
spack install curl
 #module command do not work here#module load curl
#spack  install --only dependencies rcm@develop
spack  install py-flake8
spack  install git
spack  install paraview


