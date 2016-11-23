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
#     spack install lxde-libfm
#
# You can edit this file again by typing:
#
#     spack edit lxde-libfm
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class LxdeLibfm(AutotoolsPackage):
    """LXDE PCManFM libfm component"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://wiki.lxde.org/en/PCManFM"
    url      = "http://downloads.sourceforge.net/project/pcmanfm/PCManFM%20%2B%20Libfm%20%28tarball%20release%29/LibFM/libfm-1.2.4.tar.xz"

    version('1.2.4', '74997d75e7e87dc73398746fd373bf52')

    variant('extraonly',default=False,
            description="Needed to avoid circulare dep with menucache")
    # FIXME: Add dependencies if required.
    # depends_on('m4', type='build')
    # depends_on('autoconf', type='build')
    # depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('pkg-config', type='build')
    depends_on('cairo')
    depends_on('gtkplus')
    depends_on('glib')
    depends_on('lxde-menu-cache',when='~extraonly')
    #depends_on('lxde-common')

    def configure_args(self):
       # FIXME: Add arguments other than --prefix
       # FIXME: If not needed delete the function
       args = []
       if '+extraonly' in self.spec:
           args.append('--with-extra-only')
       return args
