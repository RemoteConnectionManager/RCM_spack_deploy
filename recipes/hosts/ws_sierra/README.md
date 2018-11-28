# Deploy RCM  client development  (tested on mint )

Prerequisites: git, python

Create new base folder
    
    mkdir <base_folder>
    cd <base_folder>
    
Clone RCM source and deploy repo:

    git clone -b dev  https://github.com/RemoteConnectionManager/RCM_spack_deploy.git 
    git clone -b dev  https://github.com/RemoteConnectionManager/RCM.git
    mkdir cache
    cd RCM_spack_deploy
    ln -s ../cache .
    source recipes/hosts/ws_sierra/setup.sh dev

