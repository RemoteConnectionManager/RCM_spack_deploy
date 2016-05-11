# RCM_spack_deploy
deploy components and scripts for RCM


Git submodule experiments, following:
https://medium.com/@porteneuve/mastering-git-submodules-34c65e940407#.qv37vr398
https://medium.com/@porteneuve/getting-solid-at-git-rebase-vs-merge-4fa1a48c53aa#.3iuiwupoz

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


Take some inspiration from icebin spack setup:
https://github.com/citibeth/icebin
and
https://github.com/WireCell/wire-cell-spack