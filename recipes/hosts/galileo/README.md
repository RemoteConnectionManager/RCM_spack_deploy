# Deploy status on  hpc3

First step: clone this repo:

    git clone -b dev  https://github.com/RemoteConnectionManager/RCM_spack_deploy.git <folder name>
    cd <folder name>

link here a pre-filled cache of all downloaded artifact

    ln -s ../cache .
    source recipes/hosts/galileo/setup.sh prod

