# Deploy status on  hpc3

go to deploy and clone RCM git there

    cd deploy
    git clone https://github.com/RemoteConnectionManager/RCM.git

create a folder under deploy where put spack and install and logs
cd there

    mkdir rcm00
    cd rcm00

launch the config

    source ../../recipes/server/marconi/build_config.sh spack_dev
    # this set up commands for various steps
    $RCM_DEPLOY_COMMAND
    $RCM_DEPLOY_DEVEL_COMMAND
    # this is the command for spack development deploy
    $RCM_DEPLOY_BUILD_COMMAND
    # this is the command for build all dependencies
    $RCM_DEPLOY_SPACK_SETUP_COMMAND
    # this is the spack instance setup command
    $RCM_DEPLOY_BUILD
    # this is the command to buil just rcm in diy mode so to allow using git extracted source


