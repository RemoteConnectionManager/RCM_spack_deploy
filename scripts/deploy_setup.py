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

import util


parser = argparse.ArgumentParser(description="""
  Clone origin repository, opionally update the develop branch, integrate a list of PR and branches into a new branch
  usage examples: 
   python {scriptname} --prlist 579 984 943 946 1042 797 --branches clean/develop 'pr/(.*)'
   python {scriptname} --debug=1 --dest=../deploy/spack2 --prlist   797 -branches clean/develop 'pr/fix.*' 'pr/.*' 'wip/.*'
""".format(scriptname=sys.argv[0]), formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-d', '--debug', action='store',
                    help='debug level: warning,error,debug',
                    default='info')
parser.add_argument('--origin', action='store',
                    help='URL of the origin git repo being cloned.',
                    default='https://github.com/RemoteConnectionManager/spack.git')
parser.add_argument('--logfile', action='store',
                    help='logfile to log into.',
                    default= os.path.splitext(sys.argv[0])[0]+'.log')
parser.add_argument('--upstream', action='store',
                    help='URL of the upstream git repo.', default='https://github.com/LLNL/spack.git')

parser.add_argument('--branches', nargs='*', default=['develop'],
                    help='Regular expressions of origin branches to fetch.  The first one specified will be checked out.')

parser.add_argument('--master', action='store', default='develop',
                    help='name of the branch that will be created.')

parser.add_argument('--upstream_master', action='store', default='develop',
                    help='upstream branch to sync with.')

parser.add_argument('--dry_run', action='store_true', default=False,
                    help='do not perform any action')

parser.add_argument('--prlist', nargs='*', default=[],
                    help='Regular expressions of upstream pr to fetch and merge.')

parser.add_argument('--dest', default=argparse.SUPPRESS,
                    help="Directory to clone into.  If ends in slash, place into that directory; otherwise, \
place into subdirectory named after the URL")

args = parser.parse_args()

#print("-----args-------->", args)

# ------ Determine destination directory
destRE = re.compile('.*/(.*?).git')
repo_name = destRE.match(args.origin).group(1)

if 'dest' in args:
    dest = args.dest
    if dest[-1] == '/':
        dest = os.path.join(dest[:-1], repo_name)
else:
    dest = os.path.join('.', repo_name)

logdir=os.path.dirname(args.logfile)
if not os.path.exists( logdir ): logdir=dest

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}
loglevel=LEVELS.get(args.debug, logging.INFO)
LONGFORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() %(asctime)s] %(message)s"
SHORTFORMAT = "%(message)s"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
actual_logfile=os.path.join(logdir,os.path.basename(args.logfile))
print("logfile in "+actual_logfile)

fh = logging.FileHandler(os.path.join(logdir,os.path.basename(args.logfile)))
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(loglevel)

# create formatter and add it to the handlers
long_formatter = logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s() %(asctime)s] %(message)s")
short_formatter = logging.Formatter("%(message)s")
ch.setFormatter(short_formatter)
fh.setFormatter(long_formatter)

# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

#logging.basicConfig(filename=os.path.join(logdir,os.path.basename(args.logfile)))

#logging.basicConfig(level=loglevel)




s = StringIO.StringIO()
pprint.pprint(args, s)

logger.info("lanciato con---->"+s.getvalue())

origin_branches = util.get_branches(args.origin, branch_selection=args.branches)

upstream_branches = util.get_branches(
    args.upstream,
    branch_pattern='.*?\s+refs/pull/([0-9]*?)/head\s+',
    #branch_exclude_pattern='.*?\s+refs/pull/({branch})/merge\s+',
    branch_format_string='pull/{branch}/head',
    branch_selection=args.prlist)

# ------ Construct the regular expression used to evaluate branches
branchRE = list()
for branch in args.branches:
    branchRE.append('(' + branch + ')')
branchRE = re.compile('^(' + '|'.join(branchRE) + r')$')

# --------- Fetch them
if not os.path.exists(dest):
    os.makedirs(dest)

dev_git = util.git_repo(dest,logger = logger,dry_run=args.dry_run)

dev_git.init()
# cmd = ['git', 'init']
# subprocess.Popen(cmd, cwd=dest).wait()

dev_git.get_remotes()
dev_git.add_remote(args.origin, name='origin', fetch_branches=origin_branches)
dev_git.add_remote(args.upstream, name='upstream')

local_pr=util.trasf_match(upstream_branches,in_match='.*/([0-9]*)/(.*)',out_format='pull/{name}/clean')
#print(local_branches)

dev_git.fetch(name='origin',branches=origin_branches)

if len(origin_branches) > 0 :
    upstream_clean = origin_branches[0]
    print(upstream_clean)
    dev_git.checkout(upstream_clean)
    dev_git.sync_upstream()
    dev_git.checkout(upstream_clean,newbranch=args.master)

    dev_git.sync_upstream()

    for b in origin_branches[1:] :
        dev_git.checkout(b)
        dev_git.sync_upstream(options=['--rebase'])

    dev_git.fetch(name='upstream',branches=local_pr)

    for n,branch in local_pr.items():
        print("local_pr",n,branch)
        dev_git.checkout(branch,newbranch=branch+'_update')
        dev_git.merge(upstream_clean,comment='sync with upstream develop ')
        dev_git.checkout(args.master)
        dev_git.merge(branch+'_update',comment='merged '+branch)

    for branch in origin_branches[1:] :
        dev_git.checkout(args.master)
        dev_git.merge(branch,comment='merged '+branch)

