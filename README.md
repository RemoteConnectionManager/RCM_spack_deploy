# RCM_spack_deploy
deploy components and scripts for RCM

Try to take some inspiration from:
  * [icebin spack setup](https://github.com/citibeth/icebin)
  * [Wirecell spck build](https://github.com/WireCell/wire-cell-spack)

Currently experimenting with Git submodule, following some hints:

  * [Tutorial and setup for submodules](https://medium.com/@porteneuve/mastering-git-submodules-34c65e940407#.qv37vr398)
  * [Hints on rebase](https://medium.com/@porteneuve/getting-solid-at-git-rebase-vs-merge-4fa1a48c53aa#.3iuiwupoz)

This are command used to create first local copy and upload on github:

    git clone https://github.com/RemoteConnectionManager/RCM_spack_deploy.git
    cd RCM_spack_deploy
    git submodule init
    git submodule add https://github.com/RemoteConnectionManager/spack.git spack

    # to make git status show submodule status as well
    $ git config --global status.submoduleSummary true 

    # add the submodule, check it out and add .gitmodules
    git commit -m "Spack submodule added"
    git push
    
To check out a new copy:

    git clone --recursive https://github.com/RemoteConnectionManager/RCM_spack_deploy.git
    cd RCM_spack_deploy

To initialize repo
    
    source spack/share/spack/setup-env.sh
    spack repo add repo
    spack list


