#!/usr/bin/env bash
#spack  compiler find --scope site
spack find -l curl
spack spec -l curl
spack install curl
spack module refresh -y
moule load curl
