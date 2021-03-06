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
#
from spack import *
from distutils.dir_util import copy_tree
#from distutils.dir_util import mkpath
import llnl.util.tty as tty
import os
import shutil


def file_ok(x):
    """Any valid file, and also void value """
    if x :
        return os.path.exists(x)
    else:
        return True

class Rcm(Package):
    """Python client-server wrapper around TurboVNC to simplify 
    tunneled VNC connections to HPC clusters Remote Visualization resources,
    develope by CINECA"""

    homepage = "https://wiki.u-gov.it/confluence/pages/viewpage.action?pageId=68391634"
    url      = "https://github.com/RemoteConnectionManager/RCM/archive/0.0.1.tar.gz"

    version('v0.0.2', 'a9ee0ddfa533701a3a538011f9c2349c')
    version('v0.0.3', 'a9ee0ddfa533701a3a538011f9c2349c')
    version('v0.0.4', '215537f33ce5e17c67ec901334404c79')
    version('v0.0.5', '80c8700cfb3ba9f2709dd3ab6a4d3cdd')
    version('dev', git='https://github.com/RemoteConnectionManager/RCM.git', branch='dev')
    version('master', git='https://github.com/RemoteConnectionManager/RCM.git', branch='master')

    variant('linksource', default=False, description='link to source instead of copying scripts')
    variant('client', default=False, description='install client part')
    variant('server', default=True, description='install server part')
    variant('mesa', default=False, description='install mesa OpenGL sw emulation')
    variant('virtualgl', default=False, description='install virtualgl OpenGL interposer')



    variant(
        'configdir',
        default='config/generic/ssh',
        values=file_ok,  # Existing file here
        description='configuration directory'
    )

    # FIXME: Add dependencies if required.
    depends_on('git', when='@dev', type='build')
    depends_on('git', when='@master', type='build')
    depends_on('xkeyboard-config+xorg',  when='+server', type='run')
    # depends_on('turbovnc+x11deps ^xkeyboard-config+xorg', when='+server', type='run')
    depends_on('turbovnc+x11deps+server', when='+server', type='run')
    depends_on('turbovnc+x11deps+java~server', when='+client platform=linux', type='run')
    depends_on('turbovnc+java~x11deps~server', when='+client platform=darwin', type='run')
    # lxde dependencies
    ###########################################
    depends_on('lxde-lxterminal', when='+server', type='run')
    depends_on('lxde-icon-theme', when='+server', type='run')
    depends_on('openbox', when='+server', type='run')
    depends_on('pcmanfm', when='+server', type='run')
    depends_on('leafpad', when='+server', type='run')
    depends_on('gpicview', when='+server', type='run')
    depends_on('tint2', when='+server', type='run')

    depends_on('image-magick', when='+server', type='run')
    ###########################################
    depends_on('fluxbox', when='+server', type='run')
    depends_on('xdpyinfo', when='+server', type='run')
    depends_on('xedit', when='+server', type='run')
    depends_on('xfs', when='+server', type='run')
    depends_on('setxkbmap', when='+server', type='run')
    depends_on('xkbevd', when='+server', type='run')
    depends_on('xkbutils', when='+server', type='run')
    depends_on('xlsfonts', when='+server', type='run')
    depends_on('xfontsel', when='+server', type='run')
    depends_on('font-util fonts=font-adobe-75dpi', when='+server', type='run')
    depends_on('mesa', when='+mesa', type='run')
    depends_on('virtualgl', when='+virtualgl', type='run')
    
    depends_on('python', type='run')
    depends_on('py-six', when='+server', type='run')
    depends_on('py-paramiko', when='+client', type='run')
    depends_on('py-packaging', when='+client', type='run')
    depends_on('py-pycrypto', when='+client', type='run')
    depends_on('py-pexpect', when='+client', type='run')
    depends_on('py-pyinstaller', when='+client', type='run')
    def install(self, spec, prefix):
        rcm_source=os.path.abspath(self.stage.source_path)
        if os.path.abspath(os.path.dirname(rcm_source)) == os.path.abspath(self.stage.path):
            dest=os.path.join(os.path.abspath(self.prefix),'source')
            tty.warn('copy RCM source tree in prefix: '+rcm_source + ' -->'+dest)
            shutil.copytree(rcm_source,dest)
            rcm_source=dest
        tty.warn('source->'+rcm_source)
        tty.warn('stage->'+self.stage.path)

        if '+server' in self.spec:
            mkdirp(prefix.bin)
            configdir = spec.variants['configdir'].value
            if not os.path.exists(configdir) :
                tty.warn(' non existing configdir :' + configdir)
                configdir = os.path.join(rcm_source,
                'config/generic/ssh')
                tty.warn(' forcing configdir :' + configdir)
            if '+linksource' in self.spec:
                tty.warn('linking to source->'+rcm_source)
                os.symlink(rcm_source,
                           os.path.join(prefix,'src'))
                mkdirp(os.path.join(prefix.bin,'server'))
                os.symlink(os.path.join(rcm_source,'rcm','server','bin','server'),
                           os.path.join(prefix.bin,'server','rcm_new_server.py'))
                os.symlink(configdir, os.path.join(prefix.bin,'config'))
                os.symlink(configdir, os.path.join(rcm_source,'rcm','server','etc','site'))
            else:
                copy_tree(os.path.join(rcm_source,'rcm','server'), os.path.join(prefix.bin,'server'),verbose=1)
                copy_tree(configdir, os.path.join(prefix.bin,'config'),verbose=1)
                copy_tree(configdir, os.path.join(prefix.bin,'server','etc','site'),verbose=1)
        if '+client' in self.spec:
            rcm_client_dir=os.path.join(os.path.abspath(self.stage.source_path),'client')
            mkdirp(prefix.bin)
            for f in ['rcm_client_tk.py','rcm_client.py','rcm_protocol_client.py','rcm_utils.py','d3des.py'] :
                rcm_source_file=os.path.join(rcm_client_dir,f)
                rcm_target_file=os.path.join(prefix.bin,f)
                if '+linksource' in self.spec:
                    tty.warn('linking file :'+rcm_source_file+' -->'+rcm_target_file)
                    os.symlink(rcm_source_file, rcm_target_file)
                else:
                    shutil.copyfile(rcm_source_file, rcm_target_file)
            rcm_batch_file=os.path.join(prefix.bin,"rcm.sh")
            with open(rcm_batch_file, "w") as text_file:
                text_file.write("python %s" % os.path.join(prefix.bin,'rcm_client_tk.py'))
                mode = os.stat(rcm_batch_file).st_mode
                mode |= (mode & 0o444) >> 2
                os.chmod(rcm_batch_file, mode)

