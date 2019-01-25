spack mirror  add --scope site  common_cache file:///gpfs/work/DATA/spack/cache
spack install -v gcc@7.3.0
 spack module tcl refresh -y gcc@7.3.0
module load gcc; spack  compiler find --scope site
spack install -v openmpi
