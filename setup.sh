#! /bin/bash
# Absolute path to this script. /home/user/bin/foo.sh

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file wa
s located
done
export RCM_DEPLOY_ROOTPATH="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

source share/spack/setup-env.sh