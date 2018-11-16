#!/bin/bash
echo "HOSTPATH-->${RCM_DEPLOY_HOSTPATH}<--"
echo "GITREPO-->${RCM_GIT_PATH}<--"
echo "DESTPATH-->$RCM_DEPLOY_SPACK_PATH<--"

export RCM_DEPLOY_DEVEL_COMMAND="python ${RCM_DEPLOY_ROOTPATH}/scripts/deploy_setup.py --integration --clearconfig --debug=debug  --master $RCM_DEPLOY_MASTER_BRANCH --branches clean/develop     pr/.*  wip/.* --prlist $RCM_DEPLOY_PRLIST --dest  $RCM_DEPLOY_SPACK_PATH  --config ${RCM_DEPLOY_HOSTPATH} --install $RCM_DEPLOY_INSTALL_PATH"

export RCM_DEPLOY_COMMAND="python ${RCM_DEPLOY_ROOTPATH}/scripts/deploy_setup.py  --clearconfig --debug=debug  --master $RCM_DEPLOY_MASTER_BRANCH --branches $RCM_DEPLOY_MASTER_BRANCH --dest $RCM_DEPLOY_SPACK_PATH  --config ${RCM_DEPLOY_HOSTPATH} --install $RCM_DEPLOY_INSTALL_PATH"

echo "RCM_DEPLOY_DEVEL_COMMAND -->${RCM_DEPLOY_DEVEL_COMMAND}<--"
echo "RCM_DEPLOY_COMMAND -->${RCM_DEPLOY_COMMAND}<--"

export RCM_DEPLOY_BUILD_DEPS="spack install -v --only dependencies ${RCM_DEPLOY_SPEC}"
export RCM_DEPLOY_BUILD="spack diy --source-path ${RCM_GIT_PATH} ${RCM_DEPLOY_SPEC} ${RCM_DEPLOY_CONFIG_VARIANT}"

echo "RCM_DEPLOY_SPACK_SETUP_COMMAND -->${RCM_DEPLOY_SPACK_SETUP_COMMAND}<--"
echo "RCM_DEPLOY_BUILD_DEPS -->${RCM_DEPLOY_BUILD_DEPS}<--"
echo "RCM_DEPLOY_BUILD -->${RCM_DEPLOY_BUILD}<--"
