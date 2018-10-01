#!/usr/bin/env bash
#spack  compiler find --scope site
spack find -l curl
spack spec -l curl
spack install curl
spack module refresh -y
#module command do not work here#module load curl
spack  install --only dependencies rcm@develop
spack  install py-flake8
spack  install git
spack  install paraview
spack  install openfoam-com
spack  install rstudio

