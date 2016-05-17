#!/bin/bash
# Absolute path to this script. /home/user/bin/foo.sh

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
SCRIPTPATH="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
ROOTPATH="$( dirname "$SCRIPTPATH" )"
echo "write ${SCRIPTPATH}/intel.cfg"
echo "\
-Xlinker -rpath=${INTEL_HOME}/ipp/lib/intel64 \
-Xlinker -rpath=${INTEL_HOME}/tbb/lib/intel64/gcc4.4 \
-Xlinker -rpath=${INTEL_HOME}/mkl/lib/intel64 \
-Xlinker -rpath=${INTEL_HOME}/lib/intel64" > ${SCRIPTPATH}/intel.cfg
for v in ICCCFG ICPCCFG IFORTCFG 
 do
   export $v=${SCRIPTPATH}/intel.cfg
 done
