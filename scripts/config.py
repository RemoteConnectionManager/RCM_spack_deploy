#!/usr/bin/env python


from __future__ import print_function
import pprint, StringIO

import os
import sys
import subprocess
import io
import re
import argparse
import logging
import glob

import utils

ls=utils.log_setup()
logging.debug("__file__:" + os.path.realpath(__file__))
ls.set_args()

basepath = os.path.dirname(os.path.realpath(__file__))
logging.info("basepath-->"+basepath+"<--")
root_dir=os.path.abspath(os.path.dirname(basepath))
logging.info("root_dir-->"+root_dir+"<--")


# argfile_parser = argparse.ArgumentParser(add_help=False)
# argfile_parser.add_argument('-a','--args_file', default = os.path.join(root_dir,'config','args.yaml'))
# argfile_parser.add_argument('-c','--config_paths', nargs='*', default = [os.path.join(root_dir,'config')])
# argfile_parser.add_argument('-d','--debug', default = 'error')
# argfile_parser.add_argument('--dest', default=argparse.SUPPRESS,
#                     help="Directory to clone spack instance into.  If ends in slash, place into that directory; otherwise, \
# place into subdirectory named according to the git URL")
# argfile_args=argfile_parser.parse_known_args()[0]
#
# loglevel=LEVELS.get(argfile_args.debug, logging.INFO)
#
# mylogger.debug("before mylog setlevel")
# for l in [mylogger,logging.getLogger('utils.git_wrap'),logging.getLogger('external.hiyapyco')] :
#     l.setLevel(loglevel)
#     l.addHandler(handler)
#     l.propagate = False
#
# for l in [logging.getLogger('external.hiyapyco')]: l.setLevel(logging.INFO)
# mylogger.debug("after mylog setlevel")
# #print(sys.path)
# from external import hiyapyco
# import utils
#
# mylogger.debug("after import")



parser = argparse.ArgumentParser(description="""
  Clone origin repository, opionally update the develop branch, integrate a list of PR and branches into a new branch
  usage examples:
   python {scriptname} --prlist 579 984 943 946 1042 797 --branches clean/develop 'pr/(.*)'
   python {scriptname} --debug=1 --dest=../deploy/spack2 --prlist   797 -branches clean/develop 'pr/fix.*' 'pr/.*' 'wip/.*'
""".format(scriptname=sys.argv[0]), formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-a','--args_file', default = os.path.join(root_dir,'config','args.yaml'))
parser.add_argument('-c','--config_paths', nargs='*', default = [os.path.join(root_dir,'config')])
parser.add_argument('--logfile', action='store',
                    help='logfile to log into.',
                    default= os.path.splitext(sys.argv[0])[0]+'.log')


argfile_parser = argparse.ArgumentParser(add_help=False)
argfile_parser.add_argument('-a','--args_file', default = os.path.join(root_dir,'config','args.yaml'))
argfile_parser.add_argument('-c','--config_paths', nargs='*', default = [os.path.join(root_dir,'config')])

mylogger = logging.getLogger(__name__)
listpaths=[]
for c in argfile_parser.parse_known_args()[0].config_paths:
    mylogger.debug("config folder:"+c)
    if c[0] != '/' : c=os.path.abspath(os.path.join(root_dir,c))
    default_file=os.path.join(c,'defaults.yaml')
    if os.path.exists(default_file)  :  listpaths.append(default_file)

argsfile=argfile_parser.parse_known_args()[0].args_file
if not os.path.exists(argsfile) : argsfile = os.path.join(root_dir,'config','args.yaml')
if os.path.exists(argsfile) : listpaths.append(argsfile)
mylogger.debug("conf files-->"+str(listpaths))
mylogger.debug("---prima-------################------------")
conf = utils.hiyapyco.load(
#        *[os.path.join(argfile_parser.parse_known_args()[0].config_paths,'defaults.yaml'),
#        argfile_parser.parse_known_args()[0].args_file],
        *listpaths,
        interpolate=True,
        method=utils.hiyapyco.METHOD_MERGE,
        failonmissingfiles=False
        )
#for h in mylogger.handlers : mylogger.removeHandler(h)


mylogger.debug("---dopo-------################------------")
defaults=conf['defaults']
for d in defaults:
    mylogger.debug("default :"+d+' --> '+str(defaults[d]))

configurations=conf['configurations']
for d in configurations :
    mylogger.debug("configuration : " + d + " - " + type(configurations[d]).__name__ + "<-->" + str(configurations[d]))

conf_args=conf['args']
for a in conf_args:
  #print(a,conf_args[a])
  arguments=dict()
  arguments['help']=conf_args[a]['help']
  arguments['action']=conf_args[a]['action']
  d=conf_args[a]['default']
  #print(d, type(d).__name__)
  if d:
    if d[0]=='['  :
      #print("multimpar",a,conf_args[a]['default'])
      arguments['nargs']='*'
      arguments['default'] = eval(d)
    else:
      if  arguments['action'] == 'store_true' : arguments['default'] = eval(d)
      else: arguments['default'] = str(d)

  parser.add_argument('--'+a,**arguments)
#print("argparse.SUPPRESS-->"+argparse.SUPPRESS+"<---------------")
parser.add_argument('--dest', default=argparse.SUPPRESS,
                    help="Directory to clone spack instance into.  If ends in slash, place into that directory; otherwise, \
place into subdirectory named according to the git URL")
#parser.add_argument('--dest',
#                    help="Directory to clone into.  If ends in slash, place into that directory; otherwise, \
#place into subdirectory named after the URL")

args = parser.parse_args()


#pprint.PrettyPrinter(indent=20).pprint(conf)
#print("--------------\n",args)
for k, v in args.__dict__.iteritems():
    mylogger.debug("arg "+k+" type: "+type(v).__name__+" -->"+str(v)) # Works!
#exit()

#print("-----args-------->", args)
#print("this script-->"+__file__+"<--")

# ------ Determine destination directory
destRE = re.compile('.*/(.*?).git')
repo_name = destRE.match(args.origin).group(1)

if 'dest' in args:
    dest = args.dest
    if dest[0] != '/':
        dest = os.path.join(root_dir,dest)
    if dest[-1] == '/':
        dest = os.path.join(dest[:-1], repo_name)

else:
    dest = os.path.join(root_dir,'deploy', repo_name)

mylogger.debug("##############destination folder-->"+dest+"<--")


logdir=os.path.dirname(args.logfile)
if not os.path.exists( args.logfile ): logdir=dest
logdir=os.path.abspath(logdir)

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}
loglevel=LEVELS.get(args.debug, logging.INFO)
LONGFORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() %(asctime)s] %(message)s"
SHORTFORMAT = "##%(message)s"
# create formatters
long_formatter = logging.Formatter(LONGFORMAT)
short_formatter = logging.Formatter(SHORTFORMAT)

ll = logging.getLogger()
for h in ll.handlers :
    print("setting level ",loglevel, " and short format to handler:",h)
    h.setFormatter(short_formatter)
    h.setLevel(loglevel)
    #ll.removeHandler(h)

mylogger = logging.getLogger(__name__)
mylogger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
actual_logfile=os.path.abspath(os.path.join(os.path.dirname(logdir),os.path.basename(logdir)+'_'+os.path.basename(args.logfile)))
print("logfile in "+actual_logfile)

actual_logdir=os.path.dirname(actual_logfile)
if not os.path.exists(actual_logdir) : os.makedirs(actual_logdir)

fh = logging.FileHandler(os.path.join(actual_logfile))
fh.setLevel(logging.DEBUG)
fh.setFormatter(long_formatter)
mylogger.addHandler(fh)

# # create console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(loglevel)
#
# # create formatter and add it to the handlers
# long_formatter = logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s() %(asctime)s] %(message)s")
# short_formatter = logging.Formatter("#%(message)s")
# ch.setFormatter(short_formatter)
# fh.setFormatter(long_formatter)
#
# # add the handlers to mylogger
# for h in mylogger.handlers :
#     print("removing handler:",h)
#     mylogger.removeHandler(h)
# mylogger.addHandler(ch)
# mylogger.addHandler(fh)

#logging.basicConfig(filename=os.path.join(logdir,os.path.basename(args.logfile)))

#logging.basicConfig(level=loglevel)




s = StringIO.StringIO()
pprint.pprint(args, s)

mylogger.info("lanciato con---->"+s.getvalue())
mylogger.info("root_dir-->"+root_dir+"<--")




dev_git = utils.git_repo(dest,logger = mylogger,dry_run=args.dry_run)

if not os.path.exists(dest):
    mylogger.info("MISSING destintion_dir-->"+dest+"<-- ")
    os.makedirs(dest)

    origin_branches = utils.get_branches(args.origin, branch_selection=args.branches)

    dev_git.init()

    dev_git.get_remotes()
    dev_git.add_remote(args.origin, name='origin', fetch_branches=origin_branches)
    dev_git.add_remote(args.upstream, name='upstream')

    upstream_branches = utils.get_branches(
        args.upstream,
        branch_pattern='.*?\s+refs/pull/([0-9]*?)/head\s+',
        # branch_exclude_pattern='.*?\s+refs/pull/({branch})/merge\s+',
        branch_format_string='pull/{branch}/head',
        branch_selection=args.prlist)

    local_pr=utils.trasf_match(upstream_branches,in_match='.*/([0-9]*)/(.*)',out_format='pull/{name}/clean')

    mylogger.info("upstream_branches->"+str(upstream_branches)+"<--")

    dev_git.fetch(name='origin',branches=origin_branches)

    if args.integration:
        if len(origin_branches) > 0 :
            upstream_clean = origin_branches[0]
            print("--------------------------------------"+upstream_clean+"-----------------------")
            dev_git.checkout(upstream_clean)
            dev_git.sync_upstream()
            dev_git.checkout(upstream_clean,newbranch=args.master)

            dev_git.sync_upstream()

            for b in origin_branches[1:] :
                dev_git.checkout(b)
                dev_git.sync_upstream(options=['--rebase'])

            dev_git.fetch(name='upstream',branches=local_pr)

            for n,branch in local_pr.items():
                mylogger.info("local_pr "+ n+" "+branch)
                dev_git.checkout(branch,newbranch=branch+'_update')
                dev_git.merge(upstream_clean,comment='sync with upstream develop ')
                dev_git.checkout(args.master)
                dev_git.merge(branch+'_update',comment='merged '+branch)

            for branch in origin_branches[1:] :
                dev_git.checkout(args.master)
                dev_git.merge(branch,comment='merged '+branch)
    else:
        dev_git.fetch(name='origin',branches=[args.master])
        dev_git.checkout(args.master)

else:
    mylogger.info("Folder ->"+dest+"<- already existing, skipping git stuff")
    if args.__dict__.get('do_update',False):
        mylogger.info("Updating Folder ->"+dest+"<-")
        pull_options=[]
        for flag in args.pull_flags : pull_options.append('--'+flag)
        for b in dev_git.get_local_branches():
            dev_git.checkout(b)
            dev_git.sync_upstream(upstream='origin', master=b,options=pull_options)

########## cache handling ##############
cachedir=args.cache
mylogger.info("input cache_dir-->"+cachedir+"<--")
if not os.path.exists(cachedir):
    cachedir=os.path.abspath(os.path.join(root_dir,cachedir))
else:
    cachedir=os.path.abspath(cachedir)
mylogger.info("actual cache_dir-->"+cachedir+"<--")
try:
    os.makedirs(cachedir)
except OSError:
    if not os.path.isdir(cachedir):
        raise
#if not os.path.exists(cachedir):
#    os.makedirs(cachedir)
if os.path.exists(os.path.join(dest, 'var', 'spack')):
    deploy_cache=os.path.join(dest, 'var', 'spack','cache')
    mylogger.info("deploy cache_dir-->"+deploy_cache+"<--")
    if not os.path.exists(deploy_cache):
        os.symlink(cachedir,deploy_cache)
        mylogger.info("symlinked -->"+cachedir+"<-->"+deploy_cache)

########## install folder handling ##############
if  args.install:
    mylogger.info("find install in args-->"+args.install+"<--")
    install_dir = args.install
    if not os.path.exists(install_dir):
        install_dir = os.path.join(dest,args.install)
else:
    install_dir = os.path.join(dest,'opt','spack')
install_dir=os.path.abspath(install_dir)
if not os.path.exists(install_dir):
    mylogger.info("creting install_dir-->"+install_dir+"<--")
    os.makedirs(install_dir)
mylogger.info("install_dir-->"+install_dir+"<--")

#me=util.myintrospect(tags={'calori': 'ws_mint', 'galileo':'galileo', 'marconi':'marconi', 'eni':'eni' })

######## config path handling #################
config_path_list=[]
for configdir in args.config_paths :
    mylogger.info(" check input config dir -->"+configdir+"<--")
    for test in [ os.path.abspath(configdir), os.path.abspath(os.path.join(root_dir,configdir)), ] :
        if os.path.exists(test):
            config_path_list=[test]+config_path_list
            mylogger.info(" found config dir -->" + test + "<-- ADDED")
            break

subst=dict()
subst["RCM_DEPLOY_ROOTPATH"] = root_dir
subst["RCM_DEPLOY_INSTALLPATH"] = install_dir
subst["RCM_DEPLOY_SPACKPATH"] = dest

if args.platformconfig :
    platform_match=utils.myintrospect(tags=conf['configurations']['host_tags']).platform_tag()
    mylogger.info(" platform -->" + str(platform_match) +"<--")
    if platform_match :
        test=os.path.abspath(os.path.join(root_dir,
                                          configurations.get('base_folder',''),
                                          configurations.get('host_folder',''),
                                          platform_match,
                                          configurations.get('config_dir','')))
    if os.path.exists(test) :
        subst["RCM_DEPLOY_HOSTPATH"] = test
        #config_path_list=config_path_list + [test]
        config_path_list=[test] + config_path_list 

mylogger.info(" config_path_list -->" + str(config_path_list) )


########## merge, interpolate and write spack config files#########


spack_config_dir=os.path.abspath(os.path.join(dest,'etc','spack'))
if os.path.exists(spack_config_dir) :
    if args.clearconfig:
        mylogger.info("Clear config Folder ->"+spack_config_dir+"<-")
        for f in glob.glob(spack_config_dir+ "/*.yaml"):
            os.remove(f)

    for f in configurations.get('spack_yaml_files',[]) :
        merge_files=[]
        for p in config_path_list:
            test=os.path.abspath(os.path.join(p,f))
            if os.path.exists(test): merge_files = merge_files +[test]

        if merge_files :
            mylogger.info("configuring "+ f + " with files: "+str(merge_files))
            merged_f = utils.hiyapyco.load(
                *merge_files,
                interpolate=True,
                method=utils.hiyapyco.METHOD_MERGE,
                failonmissingfiles=True
            )

            mylogger.info("merged "+f+" yaml-->"+str(merged_f)+"<--")

            outfile = os.path.basename(f)
            target = os.path.join(spack_config_dir, outfile)
            mylogger.info(" output config_file " + outfile + "<-- ")
            if not os.path.exists(target):
                out=utils.hiyapyco.dump(merged_f, default_flow_style=False)
                templ = utils.stringtemplate(out)
                out = utils.stringtemplate(out).safe_substitute(subst)
                mylogger.info("WRITING config_file " + outfile + " -->" + target + "<-- ")
                open(target, "w").write(out)
        else :
            mylogger.info("no template file for "+ f + " : skipping ")



utils.source(os.path.join(dest,'share','spack','setup-env.sh'))
if args.runconfig :
    for p in reversed(config_path_list):
        initfile=os.path.join(p,'config.sh')
        if os.path.exists(initfile):
            mylogger.info("parsing init file-->" + initfile + "<-- ")
            f=open(initfile,'r')
            for line in f:
                line=line.lstrip()
                if len(line)>0:
                    if not line[0] == '#':
                        templ= utils.stringtemplate(line)
                        cmd=templ.safe_substitute(subst)
                        (ret,out,err)=utils.run(cmd.split(),logger=mylogger)
                        mylogger.info("  " + out )



