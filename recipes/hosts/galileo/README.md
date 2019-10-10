# Deploy status on  galileoi, support for gpu

Hint: to find out which is the order of search for .so in system libraries, do:

    /sbin/ldconfig -v 2>/dev/null | grep -v ^$'\t'

First step: clone this repo:

    git clone -b dev  https://github.com/RemoteConnectionManager/RCM_spack_deploy.git <folder name>
    cd <folder name>

Extract extrnal packages folders from installed rpm's

    cd recipes/hosts/galileo/
    bin/grab_external --prefix /tmp/nvidia_opengl/ --debug --rpm '^libglvnd' '^nvidia.*libs' '^mesa.*devel' --map '^/usr/lib' 'lib' --map '^/lib' 'lib' --map '^/usr/bin' 'bin' --map '/usr/include' 'include'

