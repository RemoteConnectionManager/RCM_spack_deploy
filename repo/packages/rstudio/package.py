##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
#     spack install rstudio
#
# You can edit this file again by typing:
#
#     spack edit rstudio
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import llnl.util.tty as tty
import distutils.dir_util
import os


class Rstudio(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/rstudio/rstudio"
    url      = "https://download1.rstudio.org/rstudio-1.1.383-x86_64-fedora.tar.gz"

    # FIXME: Add proper versions and checksums here.
    version('1.1.383.bin', 'a1ce682f868fd7cfc7b4a6011d17e43d')

    # FIXME: Add dependencies if required.
    depends_on('libxslt', type='run')
    depends_on('r', type='run')
    depends_on('mesa', type='run')

    @when('@:1.1.383.bin')
    def patch(self):
        """ Add binary .so file that are missing
            Horrible hack"""

        outdir = os.path.join(self.stage.source_path, 'bin')
        indir  = join_path(os.path.dirname(__file__), 'binary', 'linux')
        for f in os.listdir(indir):
            tty.info('Added file {0}'.format(f))
            install(join_path(indir, f), join_path(outdir, f))

    @when('@:1.1.383.bin')
    def install(self, spec, prefix):
        distutils.dir_util.copy_tree(".", prefix)

