#!/usr/bin/env python


from __future__ import print_function
import os
import sys
import subprocess
import io
import re
import argparse

import util

parser = argparse.ArgumentParser(description="""
  Clone origin repository, opionally update the develop branch, integrate a list of PR and branches into a new branch
  usage examples: 
   python test.py --prlist 579 984 943 946 1042 797 --branches clean/develop 'pr/(.*)' 
   python test.py --prlist  -579 984  797 -branches clean/develop 'pr/fix.*' 'pr/.*' 'wip/.*'
""", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--debug', action='store',
                    help='debug level',
                    default=0)
parser.add_argument('--origin', action='store',
                    help='URL of the origin git repo being cloned.',
                    default='https://github.com/RemoteConnectionManager/spack.git')
parser.add_argument('--upstream', action='store',
                    help='URL of the upstream git repo.', default='https://github.com/LLNL/spack.git')

parser.add_argument('--branches', nargs='*', default=['develop'],
                    help='Regular expressions of origin branches to fetch.  The first one specified will be checked out.')

parser.add_argument('--master', action='store', default='develop',
                    help='name of the branch that will be created.')

parser.add_argument('--upstream_master', action='store', default='develop',
                    help='upstream branch to sync with.')

parser.add_argument('--prlist', nargs='*', default=[],
                    help='Regular expressions of upstream pr to fetch and merge.')

parser.add_argument('--dest', default=argparse.SUPPRESS,
                    help="Directory to clone into.  If ends in slash, place into that directory; otherwise, \
place into subdirectory named after the URL")

args = parser.parse_args()

print("-----args-------->", args)

# ------ Determine destination directory
destRE = re.compile('.*/(.*?).git')
repo_name = destRE.match(args.origin).group(1)

if 'dest' in args:
    dest = args.dest
    if dest[-1] == '/':
        dest = os.path.join(dest[:-1], repo_name)
else:
    dest = os.path.join('.', repo_name)



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

dev_git = util.git_repo(dest,debug_level=args.debug)

dev_git.init()
# cmd = ['git', 'init']
# subprocess.Popen(cmd, cwd=dest).wait()

dev_git.get_remotes()
dev_git.add_remote(args.origin, name='origin', fetch_branches=origin_branches)
dev_git.add_remote(args.upstream, name='upstream')

local_pr=util.trasf_match(upstream_branches,in_match='.*/([0-9]*)/(.*)',out_format='pull/{name}/clean')
#print(local_branches)

dev_git.fetch(name='upstream',branches=local_pr)
dev_git.fetch(name='origin',branches=origin_branches)

