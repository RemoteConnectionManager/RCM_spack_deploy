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
module load intel/cs-xe-2015--binary
echo "ROOTPATH-->$ROOTPATH<--"
source $ROOTPATH/spack_clean/share/spack/setup-env.sh
source $SCRIPTPATH/intel/setup.sh

spack  compiler find --scope site
