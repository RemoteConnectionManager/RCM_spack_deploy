# RCM_spack_deploy
deploy components and scripts for RCM

For contributing to upstream spack, update current feature branches that will likely become PR to upstream, eventually fetch and integrate other interesting branches and integrate everything in develop integration branch like:

    cd RCM_spack_deploy
    python scripts/deploy_setup.py --integration --dest=deploy/rcm_integration --debug=debug  --branches clean/develop     pr/.*  wip/.*
    
if everything goes well, push integration on origin

    git push --all --force origin

Hints on a workflow for contributing PR to upstream Spack
  * [suggested workflow by Denis Davydov](https://groups.google.com/forum/#!topic/spack/2Rs3BMLeTFk)
  * [Denis Davydov deali project hints](https://www.google.com/url?q=https%3A%2F%2Fgithub.com%2Fdealii%2Fdealii%2Fblob%2Fmaster%2FCONTRIBUTING.md&sa=D&sntz=1&usg=AFQjCNG8i5f6CuZd6S27C1a0kGWEvtpqDg)
  * [hints on rebase a messed up spack PR](https://github.com/LLNL/spack/pull/796#issuecomment-218904402)

Spack based projects
  * [Elizabeth Fisher icebin spack setup](https://github.com/citibeth/icebin)
  * [Spack testing project, spack install examples](https://github.com/eschnett/spack-test)
  * [Wirecell spck build](https://github.com/WireCell/wire-cell-spack)




Some git hints:

    # show which branch contains a commit
    git branch --contains 86d2b2f4904f4fdbaf3e810db25a3c62799f321c

    #print the commit diff
    git show 86d2b2f4904f4fdbaf3e810db25a3c62799f321c

  * [suggestion for rebase](https://github.com/LLNL/spack/pull/1040/#issuecomment-225345722)

    #first try to pull --rebase from upstream
    git pull --rebase upstream develop


  * [rename a remote branch](https://gist.github.com/lttlrck/9628955)
    
    git branch -m pr/libxcb/pkgconfig old/libxcb/pkgconfig
    git push origin :pr/libxcb/pkgconfig
    git push --set-upstream origin old/libxcb/pkgconfig

Hints on Git submodule:
  * [Tutorial and setup for submodules](https://medium.com/@porteneuve/mastering-git-submodules-34c65e940407#.qv37vr398)
  * [other submodule tutorial](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
  * [other submodule tutorial](https://chrisjean.com/git-submodules-adding-using-removing-and-updating/)
  * [Hints on rebase](https://medium.com/@porteneuve/getting-solid-at-git-rebase-vs-merge-4fa1a48c53aa#.3iuiwupoz)

This are command used to create first local copy and upload on github:

    git clone https://github.com/RemoteConnectionManager/RCM_spack_deploy.git
    cd RCM_spack_deploy
    git submodule init
    git submodule add --name spack_clean -b clean/develop  https://github.com/RemoteConnectionManager/spack.git spack_clean
    git submodule add --name develop -b develop  https://github.com/RemoteConnectionManager/spack.git spack

    # this set up the reference to the branch to include
    git config -f .gitmodules submodule.spack.branch clean/develop
    
    # to make git status show submodule status as well, this is added in local config
    git config --local status.submoduleSummary true 
    git config --local diff.submodule log
    git config --local --add submodule.spack.update rebase

    # add the submodule, check it out and add .gitmodules
    git commit -m "Spack submodule added"
    git push
    
    # Here are functions that require new git, tested with git 2.7.4
    
    #to move submodule:
    git mv spack_clean deploy/spack_clean
    
    #remove submodule
    git rm spack
    
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
    


Other git workflow, not using submodules, run git checkout and merge PR:

    #clone clean repo 
    git clone -b clean/develop https://github.com/RemoteConnectionManager/spack.git spack_clean
    cd spack_clean
    git remote add upstream https://github.com/LLNL/spack
    


    
    



