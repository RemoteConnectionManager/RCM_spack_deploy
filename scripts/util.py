#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import subprocess
import io
import re

class git_repo:
    def __init__(self, folder,debug_level=0,stop_on_error=True):
        self.folder = os.path.abspath(folder)
        self.debug=int(debug_level)
        self.stop_on_error=stop_on_error
        print("debug level-->",self.debug)

    def run(self,cmd):
        child =  subprocess.Popen(cmd, cwd=self.folder, stdout=subprocess.PIPE)
        output = child.communicate()[0]
        ret = child.returncode
        if self.debug:
            print("executed: ",' '.join(cmd), 'result: ',ret)
            if self.debug > 1:
                print(self.debug,"output->" + output + "<-")
        return (ret,output)

    def init(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        cmd = ['git', 'rev-parse', '--show-toplevel']
        (ret,output) = self.run(cmd)
        git_root = os.path.abspath(output.strip())

        print("in path ",self.folder," git rev_parse ret: ",ret, ' git top:', git_root)
        if 0 != ret or git_root != self.folder:
            cmd = ['git', 'init']
            (ret,output) = self.run(cmd)
            print("git init in ",">>" + self.folder + "<<",">>" + git_root + "<< ret= ",ret)

    def get_remotes(self):
        cmd = ['git', 'remote']
        (ret,output) = self.run(cmd)
        remotes = list()
        for line in io.StringIO(output.decode()):
            r=line.strip()
            remotes.append(r)
            #print("-->" + r + "<--")
        return remotes

    def add_remote(self, url, name='origin', fetch_branches=[]):
#        cmd = ['git', 'remote', 'remove', name]
#        subprocess.Popen(cmd, cwd=dest).wait()
        remotes=self.get_remotes()
#        print("remotes-->",remotes,"<<-")
        if name not in self.get_remotes():
            cmd = ['git', 'remote', 'add']
            for branch in fetch_branches:
                cmd.append('-t')
                cmd.append(branch)
            cmd += [name, url]

            (ret,output) = self.run(cmd)


    def fetch(self, name='origin', branches=[]):
        cmd = [ 'git', 'fetch', name ]
        if isinstance(branches,list):
            for branch in branches:
                cmd.append(branch)
        elif isinstance(branches,dict):
            for branch in branches:
                cmd.append( branch + ':' + branches[branch])
        else:
            print('Invalid branches type: either list or dict')
            return

        (ret,output) = self.run(cmd)



# ------ List the branches on the origin
# And select only those that match our branch regexp
def get_branches(url, branch_pattern='.*?\s+refs/heads/(.*?)\s+', branch_format_string='{branch}', branch_selection=[]):
    cmd = ['git', 'ls-remote', url]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

    headRE = re.compile(branch_pattern)

    remote_branches = list()
    for line in io.StringIO(output.decode()):
        match = headRE.match(line)

        if match:
             branch = match.group(1)
            # excludeRE = re.compile(branch_exclude_pattern.format(branch=branch))
            # include=True
            # for line in io.StringIO(output.decode()):
            #     if excludeRE.match(line) :
            #         include= False
            #         print("excluded branch ",branch," line :",line)
            #         break

            # if include : remote_branches.append(branch)
             remote_branches.append(branch)
    remote_branches.sort()

    #  print('#########-->' + url)
    #  for b in remote_branches:
    #    print("       -->",b)
    # ------ Construct the regular expression used to evaluate branches
    branchRE = dict()
    for p in branch_selection:
        # branchRE.append('(' + branch + ')')
        branchRE[p] = re.compile('^(' + p + ')$')
    # branchRE = re.compile('^(' + '|'.join(branchRE) + r')$')

    # ------- Figure out which of those branches we want
    fetch_branches = list()
    checkout_branch = None
    to_match = remote_branches
    for p in branch_selection:
        unmatched = []
        for branch in to_match:
            match2 = branchRE[p].match(branch)
            if match2:
                br_name = branch_format_string.format(branch=branch)
                #        if match2.group(2) and checkout_branch is None:
                #          checkout_branch = br_name
                fetch_branches.append(br_name)
            else:
                unmatched.append(branch)
        to_match = unmatched



    #  print("checkout-->",checkout_branch)
    for b in fetch_branches:
        print('{0} fetch-->'.format(url), b)

    return fetch_branches

def trasf_match(in_list,in_match='(.*)',out_format='{name}'):
    out=dict()
    in_RE = re.compile(in_match)
    for entry in in_list:
        match = in_RE.match(entry)
        if match:
            if 0 < len(match.groups()):
                name = match.group(1)
                out[entry] = out_format.format(name=name)
    return(out)
