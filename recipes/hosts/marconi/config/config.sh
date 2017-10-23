#!/usr/bin/env bash
spack repo add @{RCM_DEPLOY_ROOTPATH}/repo --scope site
spack  compiler find --scope site
#spack info rcm
#spack install --verbose py-flake8
#spack find
#spack module  rm -y
#spack module refresh -y
