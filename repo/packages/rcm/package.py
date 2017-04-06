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
#     spack install rcm
#
# You can edit this file again by typing:
#
#     spack edit rcm
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
from distutils.dir_util import copy_tree
#from distutils.dir_util import mkpath
import llnl.util.tty as tty
import os


class Rcm(Package):
    """Python client-server wrapper around TurboVNC to simplify 
    tunneled VNC connections to HPC clusters Remote Visualization resources,
    develope by CINECA"""

    homepage = "https://wiki.u-gov.it/confluence/pages/viewpage.action?pageId=68391634"
    url      = "https://github.com/RemoteConnectionManager/RCM/archive/0.0.1.tar.gz"

    version('0.0.1', '658770296b4a1ccb5af28c9aa1545f7d')
    version('develop', git='https://github.com/RemoteConnectionManager/RCM.git')

    variant('linksource', default=False, description='link to source instead of copying scripts')
    variant('client', default=False, description='install client part')
    variant('server', default=True, description='install server part')

    # FIXME: Add dependencies if required.
    depends_on('turbovnc', when='+server', type='run')
    depends_on('lxde-lxterminal', when='+server', type='run')
    depends_on('fluxbox', when='+server', type='run')
    depends_on('xdpyinfo', when='+server', type='run')
    depends_on('xedit', when='+server', type='run')
    depends_on('xfs', when='+server', type='run')
    depends_on('setxkbmap', when='+server', type='run')
    depends_on('xkbevd', when='+server', type='run')
    depends_on('xkbutils', when='+server', type='run')
    depends_on('xkbcomp', when='+server', type='run')
    depends_on('xlsfonts', when='+server', type='run')
    depends_on('xfontsel', when='+server', type='run')
    depends_on('font-adobe-75dpi', when='+server', type='run')
    depends_on('mesa+gallium', when='+server', type='run')
    
    depends_on('python+tk', when='+client', type='run')
    depends_on('py-paramiko', when='+client', type='run')
    depends_on('py-pycrypto', when='+client', type='run')
    depends_on('py-pexpect', when='+client', type='run')
    def install(self, spec, prefix):
        # Sublime text comes as a pre-compiled binary.
        #print("sono qui!!!! in "+os.path.abspath('server')+'<--->'+prefix.bin)
#        mkpath(prefix.bin)
        if '+server' in self.spec:
            mkdirp(prefix.bin)
            if '+linksource' in self.spec:
                server_source=os.path.abspath(self.stage.source_path)
                tty.warn('linking to source->'+server_source)
                os.symlink(os.path.join(server_source,'server'),
                           os.path.join(prefix.bin,'server'))
                os.symlink(os.path.join(server_source,'config/generic/ssh'),
                           os.path.join(prefix.bin,'config'))
            else:
                copy_tree('server', os.path.join(prefix.bin,'server'),verbose=1)
                copy_tree('config/generic/ssh', os.path.join(prefix.bin,'config'),verbose=1)
        if '+client' in self.spec:
            mkdirp(prefix.bin)
            rcm_batch_file=os.path.join(prefix.bin,"rcm.sh")
            with open(rcm_batch_file, "w") as text_file:
                text_file.write("python %s" % os.path.join(os.path.abspath(self.stage.source_path),'client','rcm_client_tk.py'))
                mode = os.stat(rcm_batch_file).st_mode
                mode |= (mode & 0o444) >> 2
                os.chmod(rcm_batch_file, mode)

