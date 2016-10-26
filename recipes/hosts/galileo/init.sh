#!/bin/bash
spack config --scope site get bad_section_name

#add system compiler
spack  compiler find --scope site    

module load profile/advanced

m_compilers=(
gnu/4.9.2
intel/cs-xe-2015--binary
intel/pe-xe-2016--binary
intel/pe-xe-2017--binary
)

for compiler in "${m_compilers[@]}"
do
  #add another compiler
  echo "trying to load in spack compiler: $compiler "
  module load ${compiler}
  spack  compiler find --scope site
  module unload ${compiler}
done

spack config --scope site get compilers

#symbolic link to cache folder
ln -s -f ${RCM_DEPLOY_ROOTPATH}/cache var/spack/cache

#add site specific module configuration
ln -s -f ${RCM_DEPLOY_ROOTPATH}/config/modules.yaml etc/spack/modules.yaml
