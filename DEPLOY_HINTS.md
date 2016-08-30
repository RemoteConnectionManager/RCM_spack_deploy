Spack based projects
  * [Elizabeth Fisher icebin spack setup](https://github.com/citibeth/icebin)
  * [Spack testing project, spack install examples](https://github.com/eschnett/spack-test)
  * [Wirecell spck build](https://github.com/WireCell/wire-cell-spack)
  
Some examples of Spack customization:
  * [some example of package.yaml](https://github.com/LLNL/spack/issues/1505)
  * [hints for intel compiling](https://groups.google.com/forum/#!topic/spack/NxyNTAZyMQg)


To initialize the spack copy 
    
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

