# Deploy status on  hpc3

go to deploy and clone RCM git there

    cd deploy
    git clone https://github.com/RemoteConnectionManager/RCM.git

create a folder under deploy where put spack and install and logs
cd there

    mkdir rcm00
    cd rcm00

launch the config

    source ../../recipes/hosts/eni/build_config.sh
    $RCM_DEPLOY_COMMAND
    cd spack/
    source share/spack/setup-env.sh 
    spack install -v --only dependencies rcm@develop+linksource 


