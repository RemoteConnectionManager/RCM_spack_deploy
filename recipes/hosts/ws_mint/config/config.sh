#!/usr/bin/env bash
spack repo add @{RCM_DEPLOY_ROOTPATH}/repo --scope site
spack  compiler find --scope site
#spack info rcm
spack install environment-modules~X
spack install py-flake8
spack install --only dependencies rcm@develop+client +linksource -server
#spack find
#spack module  rm -y
spack module refresh -y
#spack diy --source-path /kubuntu/home/lcalori/spack/RCM rcm@develop+client +linksource -server
