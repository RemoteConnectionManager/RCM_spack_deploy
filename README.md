# RCM_spack_deploy
deploy components and scripts for RCM


Git submodule experiments, following:
https://medium.com/@porteneuve/mastering-git-submodules-34c65e940407#.qv37vr398

This has been created with:
    $ git clone https://github.com/RemoteConnectionManager/RCM_spack_deploy.git
    $ cd RCM_spack_deploy
    $ git submodule init
    $ git submodule add https://github.com/RemoteConnectionManager/spack.git spack
    # to make git status show submodule status as well
    $ git config --global status.submoduleSummary true 
    # add the submodule, check it out and add .gitmodules
    $ git commit -m "Spack submodule added"
    $ git push

To check out:
    $ git clone --recursive https://github.com/RemoteConnectionManager/RCM_spack_deploy.git
    $ cd RCM_spack_deploy


    $ source spack/share/spack/setup-env.sh
    $ spack repo add repo
    $ spack list
