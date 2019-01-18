# RCM_spack_deploy
deploy components and scripts for RCM

First step: clone this repo:

    git clone  https://github.com/RemoteConnectionManager/RCM_spack_deploy.git <folder name>

    
Short story:

    cd <folder name>
    bin/spack-deploy   --workdir deploy/base_spack_devel/ gitmanager deploy 
    bin/spack-deploy   --workdir deploy/base_spack_devel/ spackmanager config_setup

More info can be found in:

    recipes/hosts/<host>/README.md

  * [Git hints](https://github.com/RemoteConnectionManager/RCM_spack_deploy/blob/master/GIT_HINTS.md)
  * [Deployment hints](https://github.com/RemoteConnectionManager/RCM_spack_deploy/blob/master/DEPLOY_HINTS.md)
  * [Old README](https://github.com/RemoteConnectionManager/RCM_spack_deploy/blob/master/old_stuff/README.md)

