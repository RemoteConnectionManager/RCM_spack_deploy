#!/usr/bin/env bash
spack repo add @{RCM_DEPLOY_ROOTPATH}/repo --scope site
spack  compiler find --scope site
#spack info rcm
spack spec py-flake8
spack spec rcm@develop+client +linksource -server
spack install -v environment-modules~X
spack install -v py-flake8 ^python+tk
spack install --only dependencies rcm@develop+client +linksource -server
#spack diy --source-path /kubuntu/home/lcalori/spack/RCM rcm@develop+client +linksource -server
#spack module refresh -y
#spack find
#spack module  rm -y
