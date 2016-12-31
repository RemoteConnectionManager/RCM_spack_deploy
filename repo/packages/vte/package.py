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
#     spack install vte
#
# You can edit this file again by typing:
#
#     spack edit vte
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Vte(AutotoolsPackage):
    """The VTE package contains a termcap file implementation for terminal emulators"""

    homepage = "http://www.linuxfromscratch.org/blfs/view/svn/gnome/vte.html"
    url      = "http://ftp.gnome.org/pub/gnome/sources/vte/0.28/vte-0.28.2.tar.xz"
    version('0.28.2', '497f26e457308649e6ece32b3bb142ff')

    # FIXME: Add dependencies if required.
    # depends_on('m4', type='build')
    # depends_on('autoconf', type='build')
    # depends_on('automake', type='build')
    # depends_on('libtool', type='build')
    depends_on('binutils', type='build')
    depends_on('libtool', type='build')
    depends_on('pkg-config', type='build')
    depends_on('gtkplus+X')
    depends_on('glib')
    #depends_on('pcre2')
    #depends_on('libxml2')
#    depends_on('libx11')
#    depends_on('libice')
#    depends_on('libxext')
#    depends_on('libxfixes')
#    depends_on('libxdamage')
#    depends_on('libxrender')
#    depends_on('libsm')

#    def configure_args(self):
#       args = []
#       return args
