#spack install -v gcc@7.3.0
#module load gcc; spack  compiler find --scope site
spack spec -l curl
spack install curl
spack module tcl refresh -y curl
