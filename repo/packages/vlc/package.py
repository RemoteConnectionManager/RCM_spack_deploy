##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install vlc
#
# You can edit this file again by typing:
#
#     spack edit vlc
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Vlc(AutotoolsPackage):
    """ VideoLAN media player"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://wiki.videolan.org"
    url      = "ftp://ftp.videolan.org/pub/videolan/vlc/2.2.4/vlc-2.2.4.tar.xz"

    version('2.2.4', '55666c9898f658c7fcca12725bf7dd1b')

    variant('lua',         default=False,  description='Use Lua plugin')

    patch('lua_new.patch', when='@:2.2.4^lua@3.7:')

    # FIXME: Add dependencies if required.
    # depends_on('m4', type='build')
    # depends_on('autoconf', type='build')
    # depends_on('automake', type='build')
    # depends_on('libtool', type='build')
    depends_on('lua', when='+lua')
    depends_on('libx11')
    depends_on('libxcb')
    depends_on('fontconfig')
    depends_on('freetype')
    depends_on('sdl2')
    depends_on('sdl2-image')
    depends_on('qt')
    depends_on('ffmpeg@2.8.10')
    depends_on('libgcrypt')


    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete the function
        args = ["--disable-mad","--with-x","--enable-xcb","--disable-a52","--disable-alsa","--disable-lua"]
        return args
