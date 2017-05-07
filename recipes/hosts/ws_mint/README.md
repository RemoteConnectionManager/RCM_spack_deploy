# Deploy status on  linux client ( MINT )

go to deploy and clone RCM git there

    cd deploy
    git clone https://github.com/RemoteConnectionManager/RCM.git

create a folder under deploy where put spack and install and logs
cd there

    mkdir rcm00
    cd rcm00

launch the config

    source ../../recipes/hosts/ws_mint/build_config.sh
    $RCM_DEPLOY_COMMAND
    git clone https://github.com/RemoteConnectionManager/RCM.git $RCM_GIT_PATH
    cd spack/
    source share/spack/setup-env.sh 
    spack diy --source-path $RCM_GIT_PATH rcm@develop+client +linksource -server
    


