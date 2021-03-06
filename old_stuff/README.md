# RCM_spack_deploy
deploy components and scripts for RCM

  * [Git hints](https://github.com/RemoteConnectionManager/RCM_spack_deploy/blob/master/GIT_HINTS.md)
  * [Deployment hints](https://github.com/RemoteConnectionManager/RCM_spack_deploy/blob/master/DEPLOY_HINTS.md)

Try to take some inspiration from:
  * [icebin spack setup](https://github.com/citibeth/icebin)
  * [testing project](https://github.com/eschnett/spack-test)
  * [Wirecell spck build](https://github.com/WireCell/wire-cell-spack)
  * [hints on rebase a messed up spack PR](https://github.com/LLNL/spack/pull/796#issuecomment-218904402)
  * [some example of package.yaml](https://github.com/LLNL/spack/issues/1505)
  * [hints for intel compiling](https://groups.google.com/forum/#!topic/spack/NxyNTAZyMQg)


Currently experimenting with Git submodule, following some hints:

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
    
To initialize repo
    
    #go into top spack folder (inside deploy)
    #cd deploy/spack_test
    
    source share/spack/setup-env.sh
    spack  config --site  get bad_section_name

    #add system compiler
    spack  compiler find --scope site    
    #print what has been found
    spack  config --site  get compilers
    
    #add our our package repo folder
    spack repo add ../../repo --scope site
    #print what has been added
    spack  config --site  get repos

    #list all available packages   
    spack list
    


Other git workflow, not using submodules, run git checkout and merge PR:

    #clone clean repo 
    git clone -b clean/develop https://github.com/RemoteConnectionManager/spack.git spack_clean
    cd spack_clean
    git remote add upstream https://github.com/LLNL/spack
    
    
Useful pr to integrate
946 : intel_compiler
579 : cache

git fetch upstream pull/946/head:pull/946/clean
git checkout pull/946/clean
git checkout -b pull/946/update
git merge -m "sync to develop" clean/develop

#######################################

## git hints:

# show which branch contains a commit
git branch --contains 86d2b2f4904f4fdbaf3e810db25a3c62799f321c

#print the commit diff
git show 86d2b2f4904f4fdbaf3e810db25a3c62799f321c

#################   suggestion for rebase  ##############
https://github.com/LLNL/spack/pull/1040/#issuecomment-225345722

#first try to pull --rebase from upstream
git pull --rebase upstream develop


################ rename a remote branch ############
#from https://gist.github.com/lttlrck/9628955
git branch -m pr/libxcb/pkgconfig old/libxcb/pkgconfig
git push origin :pr/libxcb/pkgconfig
git push --set-upstream origin old/libxcb/pkgconfig

