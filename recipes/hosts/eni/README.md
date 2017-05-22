# Deploy status on  hpc3

First step: clone this repo:

    git clone  https://github.com/RemoteConnectionManager/RCM_spack_deploy.git <folder name>
    cd <folder name>


go to deploy and clone RCM source git there

    cd deploy
    git clone https://github.com/RemoteConnectionManager/RCM.git

create a folder under deploy where put spack and install and logs, cd there

    mkdir rcm00
    cd rcm00

launch the config

    source ../../recipes/hosts/eni/build_config.sh
    $RCM_DEPLOY_COMMAND
    cd spack3/
    source share/spack/setup-env.sh 
    spack install -v --only dependencies rcm@develop+linksource+virtualgl 
    spack diy --source-path $RCM_GIT_PATH rcm@develop+linksource+virtualgl configdir=${RCM_GIT_PATH}/config/eni/ssh

P.S. this procedure require ability to download from internet all the needed source tarballs,
in case of restriction, better define a  pre-filled cache folder
