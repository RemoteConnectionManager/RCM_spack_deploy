#!/usr/bin/env bash
spack repo add @{RCM_DEPLOY_ROOTPATH}/repo --scope site
spack  compiler find --scope site
#spack info rcm
spack install py-flake8
spack install environment-modules~X
spack install --only dependencies rcm+client -server
#spack find
#spack module  rm -y
spack module refresh -y