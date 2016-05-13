# RCM_spack_deploy
deploy components and scripts for RCM

Try to take some inspiration from:
  * [icebin spack setup](https://github.com/citibeth/icebin)
  * [Wirecell spck build](https://github.com/WireCell/wire-cell-spack)
  * [hints on rebase a messed up spack PR](https://github.com/LLNL/spack/pull/796#issuecomment-218904402)

Currently experimenting with Git submodule, following some hints:

  * [Tutorial and setup for submodules](https://medium.com/@porteneuve/mastering-git-submodules-34c65e940407#.qv37vr398)
  * [other submodule tutorial](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
  * [other submodule tutorial](https://chrisjean.com/git-submodules-adding-using-removing-and-updating/)
  * [Hints on rebase](https://medium.com/@porteneuve/getting-solid-at-git-rebase-vs-merge-4fa1a48c53aa#.3iuiwupoz)

This are command used to create first local copy and upload on github:

    git clone https://github.com/RemoteConnectionManager/RCM_spack_deploy.git
    cd RCM_spack_deploy
    git submodule init
    git submodule add https://github.com/RemoteConnectionManager/spack.git spack

    # this set up the reference to the branch to include
    git config -f .gitmodules submodule.spack.branch clean/develop
    
    # to make git status show submodule status as well, this is added in local config
    git config --local status.submoduleSummary true 
    git config --local diff.submodule log
    git config --local --add submodule.spack.update rebase

    # add the submodule, check it out and add .gitmodules
    git commit -m "Spack submodule added"
    git push
    
To check out a new copy:

    git clone --recursive https://github.com/RemoteConnectionManager/RCM_spack_deploy.git
    cd RCM_spack_deploy
    git config --local status.submoduleSummary true
    git config --local diff.submodule log

    cd spack
    git remote add upstream https://github.com/LLNL/spack
    git checkout clean/develop
    git pull --ff-only upstream develop
    cd ..
    git commit spack -m "updating clean/develop to upstream"
    
To initialize repo
    
    source spack/share/spack/setup-env.sh
    spack repo add repo
    spack list


