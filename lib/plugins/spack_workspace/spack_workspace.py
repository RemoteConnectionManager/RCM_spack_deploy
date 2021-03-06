import os
import glob
import logging

#lib_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib')
#if not lib_path in sys.path:
#    sys.path.append(lib_path)

import utils
import cascade_yaml_config


logging.debug("imported __file__:" + os.path.realpath(__file__))


def is_spack_root(path):
    return os.path.exists(os.path.join(path, 'bin', 'spack'))


class SpackWorkspaceManager(cascade_yaml_config.ArgparseSubcommandManager):

    def __init__(self, **kwargs):
        super(SpackWorkspaceManager, self).__init__(**kwargs)
        for par in kwargs:
            self.logger.debug("init par "+ par+" --> "+str(kwargs[par]))



    def list(self, base_path=''):
        if not base_path:
            base_path = self.base_path
        else:
            if base_path[0] != '/':
                base_path = os.path.join(self.base_path, base_path)
        base_path = os.path.abspath(base_path)
        print('Searching workspaces into:', base_path)
        for root, dirs, files in os.walk(base_path, topdown=True):
            if is_spack_root(root):
                print(" OOOOOOOOOOOOO list OOOOO found spack folder ", root)
                del dirs

    def remove(self, uuid_):
        path = os.path.join(self.base_path, str(uuid_))
        try:
            os.rmdir(path)
        except OSError:
            print('error: failed to remove the directory ' + path)


    def config_setup(self,
                     spack_root='spack',
                     out_config_dir = os.path.join('etc','spack'),
                     cache='cache',
                     bincache='bincache',
                     install='install',
                     modules='modules',
                     clearconfig=True,
                     runconfig=False):



        # print("@@@@@@@@@@@@@@@@@@@@",self.dry_run)
        if spack_root [0] != '/':
            dest = os.path.join(self.base_path, spack_root)
        else:
            dest = spack_root


        ########## cache handling ##############
        cachedir=cache
        self.logger.debug("input cache_dir-->"+cachedir+"<--")
        if not os.path.exists(cachedir):
            cachedir=os.path.abspath(os.path.join(self.base_path,cachedir))
        else:
            cachedir=os.path.abspath(cachedir)
        self.logger.debug("actual cache_dir-->"+cachedir+"<--")
        try:
            os.makedirs(cachedir)
        except OSError:
            if not os.path.isdir(cachedir):
                raise
        #if not os.path.exists(cachedir):
        #    os.makedirs(cachedir)
        if os.path.exists(os.path.join(dest, 'var', 'spack')):
            deploy_cache=os.path.join(dest, 'var', 'spack','cache')
            self.logger.debug("deploy cache_dir-->"+deploy_cache+"<--")
            if not os.path.exists(deploy_cache):
                os.symlink(cachedir,deploy_cache)
                self.logger.info("symlinked -->"+cachedir+"<-->"+deploy_cache)

        ########## install folder handling ##############
        if  install:
            self.logger.debug("find install in args-->"+install+"<--")
            if install[0] != '/':
                install_dir = os.path.join(self.base_path, install)
            else:
                install_dir = install
        else:
            install_dir = os.path.join(dest,'opt','spack')
        install_dir=os.path.abspath(install_dir)
        if not os.path.exists(install_dir):
            self.logger.info("creating install_dir-->"+install_dir+"<--")
            os.makedirs(install_dir)
        self.logger.debug("install_dir-->"+install_dir+"<--")


        ########## modules folder handling ##############
        if  modules:
            self.logger.debug("find modules in args-->" + modules + "<--")
            if modules[0] != '/':
                modules_dir = os.path.join(self.base_path, modules)
            else:
                modules_dir = modules
            modules_dir=os.path.abspath(modules_dir)
            if not os.path.exists(modules_dir):
                self.logger.info("creating modules_dir-->"+modules_dir+"<--")
                os.makedirs(modules_dir)
            self.logger.debug("modules_dir-->"+modules_dir+"<--")



        ######## config path handling #################
        # config_path_list=
        # for configdir in self.args.config_paths :
        #     self.logger.info(" check input config dir -->"+configdir+"<--")
        #     for test in [ os.path.abspath(configdir), os.path.abspath(os.path.join(root_dir,configdir)), ] :
        #         if os.path.exists(test):
        #             config_path_list=[test]+config_path_list
        #             self.logger.info(" found config dir -->" + test + "<-- ADDED")
        #             break
        #
        subst=dict()
        subst["RCM_DEPLOY_ROOTPATH"] = self.root_path
        subst["RCM_DEPLOY_INSTALLPATH"] = install_dir
        subst["RCM_DEPLOY_MODULESPATH"] = modules_dir
        subst["RCM_DEPLOY_SPACKPATH"] = dest
        #
        # if platformconfig :
        #     platform_match=utils.myintrospect(tags=conf['configurations']['host_tags']).platform_tag()
        #     self.logger.info(" platform -->" + str(platform_match) +"<--")
        #     if platform_match :
        #         test=os.path.abspath(os.path.join(root_dir,
        #                                           configurations.get('base_folder',''),
        #                                           configurations.get('host_folder',''),
        #                                           platform_match,
        #                                           configurations.get('config_dir','')))
        if len(self.platform_folders) > 0 :
            subst["RCM_DEPLOY_HOSTPATH"] = self.platform_folders[0]
            if self.platform_folders[0] not in self.config_folders:
                self.logger.warning("missing " + str(self.platform_folders[0]) )
            #config_path_list=config_path_list + [test]
            #config_path_list=[test] + config_path_list

        config_path_list = self.plugin_folders + self.config_folders
        self.logger.debug(" config_path_list -->" + str(config_path_list) )


        ########## merge, interpolate and write spack config files#########

        if modules:
            self.logger.debug("find modules in args-->" + modules + "<--")
            if modules[0] != '/':
                modules_dir = os.path.join(self.base_path, modules)
            else:
                modules_dir = modules
            modules_dir = os.path.abspath(modules_dir)

        if out_config_dir:
            if out_config_dir[0] != '/':
                spack_config_dir = os.path.abspath(os.path.join(dest, out_config_dir))
            else:
                os.makedirs(out_config_dir)
                spack_config_dir = out_config_dir

        if os.path.exists(spack_config_dir) :
            if clearconfig:
                self.logger.info("Clear config Folder ->"+spack_config_dir+"<-")
                for f in glob.glob(spack_config_dir+ "/*.yaml"):
                    os.remove(f)

            for f in self.manager_conf.get('config', dict()).get('spack_yaml_files',[]) :
                merge_files=[]
                for p in config_path_list:
                    test=os.path.abspath(os.path.join(p,f))
                    if os.path.exists(test): merge_files = merge_files +[test]

                if merge_files :
                    self.logger.debug("configuring "+ f + " with files: "+str(merge_files))
                    merged_f = utils.hiyapyco.load(
                        *merge_files,
                        interpolate=True,
                        method=utils.hiyapyco.METHOD_MERGE,
                        failonmissingfiles=True
                    )

                    self.logger.debug("merged "+f+" yaml-->"+str(merged_f)+"<--")

                    outfile = os.path.basename(f)
                    target = os.path.join(spack_config_dir, outfile)
                    self.logger.debug(" output config_file " + outfile + "<-- ")
                    if not os.path.exists(target):
                        out=utils.hiyapyco.dump(merged_f, default_flow_style=False)
                        out = utils.stringtemplate(out).safe_substitute(subst)
                        self.logger.info("WRITING config_file " + outfile + " -->" + target + "<-- ")
                        open(target, "w").write(out)
                else :
                    self.logger.info("no template file for "+ f + " : skipping ")



        utils.source(os.path.join(dest,'share','spack','setup-env.sh'))
        if runconfig :
            for p in config_path_list:
                initfile=os.path.abspath(os.path.join(p,'config.sh'))
                if os.path.exists(initfile):
                    self.logger.info("executing init file-->" + initfile + "<-- ")

        #            self.logger.info("parsing init file-->" + initfile + "<-- ")
        ##            (ret,out,err)=utils.run(['/bin/bash', initfile], logger=self.logger)
        ##            self.logger.info("  " + out )
                    f=open(initfile,'r')
                    for line in f:
                        line=line.lstrip()
                        if len(line)>0:
                            if not line[0] == '#':
                                templ= utils.stringtemplate(line)
                                cmd=templ.safe_substitute(subst)
        #                        (ret,out,err)=utils.run(cmd.split(),logger=self.logger)
                                (ret,out,err)=utils.run(['/bin/bash', '-c', cmd],
                                                        logger=self.logger,
                                                        pipe_output=True
                                                        )
                                self.logger.debug("  " + out )

            for p in config_path_list:
                initfile=os.path.join(p,'install.sh')
                if os.path.exists(initfile):
                    self.logger.info("parsing init file-->" + initfile + "<-- ")
                    f=open(initfile,'r')
                    for line in f:
                        line=line.lstrip()
                        if len(line)>0:
                            if not line[0] == '#':
                                templ= utils.stringtemplate(line)
                                cmd=templ.safe_substitute(subst)
                                (ret,out,err)=utils.run(cmd.split(),logger=self.logger)
                                self.logger.info("  " + out )
