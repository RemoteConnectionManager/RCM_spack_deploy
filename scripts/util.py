#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import subprocess
import io
import re
import collections
import logging
import json

import socket
import platform

def run(cmd,logger=None,stop_on_error=True,dry_run=False,folder='.'):
    logger = logger or logging.getLogger(__name__)
    if not cmd :
        logger.warning("skipping empty command")
        return (0, '','')
    logger.info("running-->"+' '.join(cmd)+"<-")
    if not dry_run :
        myprocess = subprocess.Popen(cmd, cwd=folder,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr = myprocess.communicate()
        myprocess.wait()
        ret = myprocess.returncode
        if ret:
            #print("ERROR:",ret,"Exiting")
            logger.error("ERROR CODE : " + str(ret) + '\n'+stderr+'\nExit...\n')
            if stop_on_error :
                sys.exit()
        return (ret,stdout,stderr)

    else:
        logger.info("DRY RUN... nothing done")
        return (0, '','')


def source(sourcefile):
    if os.path.exists(sourcefile) :
        source = 'source '+ sourcefile
        dump = sys.executable + ' -c "import os, json;print json.dumps(dict(os.environ))"'
        pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s' %(source,dump)], stdout=subprocess.PIPE)
        env = json.loads(pipe.stdout.read())
        os.environ = env
    else:
        print("### NON EXISTING ",sourcefile)
         

class baseintrospect:
    def __init__(self):
        self.sysintro=dict()
        self.sysintro['pyver']=platform.python_version()
        self.sysintro['pyinterp']=sys.executable
        self.sysintro['sysplatform']=platform.platform()
        self.sysintro['commandline']=' '.join(sys.argv)
        self.sysintro['workdir']=os.path.abspath('.')
        self.sysintro['hostname']=socket.getfqdn()

class commandintrospect(baseintrospect):
    def __init__(self,commands=[]):
	baseintrospect.__init__(self)
        self.commands=dict()
        for c in commands:
            self.test(c)

    def test(self,cmd,key=None):
        try : 
            (ret,o,e)=run(cmd.split(),stop_on_error=False)
            if not e :
                if not key : key=cmd
                self.commands[key]=o.strip()
        except :
            pass

class myintrospect(commandintrospect):
    def __init__(self,tags={}):

        commandintrospect.__init__(self,['git --version'])

        self.test('git config --get remote.origin.url',key='giturl')
        self.tags=tags

    def platform_tag(self):
        hostname=self.sysintro['hostname']
        for k in self.tags:
            m=re.search(k,hostname)
            if m : return self.tags[k]
        return(None)


    #     (out,err)=run('svn info '+self.sysintro['workdir'])
    #     for (cmd,match) in [("svnurl","URL: "),("svnauthor","Last Changed Author: ")]:
    #         for line in out.splitlines():
	 #        if match in line:
		#     self.commands[cmd] = line[len(match):]
		#     break
    #
    # def reproduce_string(self,comment=''):
    #     out = comment+"module load ba\n"
    #     try:
    #         revision=int(self.commands['svnrevision'])
    #     except :
    #         print "WARNING svn not clean"
    #         c=re.compile('(^[0-9]*)')
    #         m=c.match(self.commands['svnrevision'])
    #         revision=m.groups()[0]
    #     out +=comment+"svn co "+self.commands['svnurl']+'@'+str(revision)+" my_common_source\n"
    #     out +=comment+"cd my_common_source\n"
    #     out +=comment+self.sysintro['pyinterp']+' '+self.sysintro['commandline']+'\n'
    #     return out


class git_repo:
    def __init__(self, folder, logger=None,stop_on_error=True,dry_run=False):
        self.folder = os.path.abspath(folder)
        self.logger = logger or logging.getLogger(__name__)
        self.stop_on_error=stop_on_error
        self.dry_run=dry_run
        #print("debug level-->",self.debug)

    def run(self,cmd):
        (ret,out,err)=run(cmd,logger=self.logger,dry_run=self.dry_run,stop_on_error=self.stop_on_error,folder=self.folder)
        return (ret,out)

    def init(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        cmd = ['git', 'rev-parse', '--show-toplevel']
        (ret,output) = self.run(cmd)
        git_root = os.path.abspath(output.strip())

        #print("in path ",self.folder," git rev_parse ret: ",ret, ' git top:', git_root)
        self.logger.info("in path "+self.folder+" git rev_parse ret: "+str(ret)+ ' git top:'+ git_root)
        if 0 != ret or git_root != self.folder:
            cmd = ['git', 'init']
            (ret,output) = self.run(cmd)
            self.logger.info("git init in >>" + self.folder + "<< >>" + git_root + "<< ret= "+ str(ret))
            #print("git init in ",">>" + self.folder + "<<",">>" + git_root + "<< ret= ",ret)

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
        remotes=self.get_remotes()
        #if self.debug : print("remotes-->",remotes,"<<-")
        self.logger.debug("remotes-->"+str(remotes)+"<<-")
        if name not in self.get_remotes():
            cmd = ['git', 'remote', 'add']
            for branch in fetch_branches:
                cmd.append('-t')
                cmd.append(branch)
            cmd += [name, url]

            (ret,output) = self.run(cmd)


    def fetch(self, name='origin', prefix='',  branches=[]):
        cmd = [ 'git', 'fetch', name ]

        if isinstance(branches,list):
            for branch in branches:
 #               cmd.append(branch)
                cmd.append( branch + ':' + prefix.format(name=name) + branch)
        elif isinstance(branches,dict):
            for branch in branches:
                cmd.append( branch + ':' + prefix.format(name=name) + branches[branch])
        else:
            self.logger.error('Invalid branches type: either list or dict')

            return

        (ret,output) = self.run(cmd)

    def checkout(self, branch, newbranch=None):
        cmd = [ 'git', 'checkout', branch ]
        if newbranch: cmd.extend(['-b', newbranch])
        (ret,output) = self.run(cmd)

    def sync_upstream(self, upstream='upstream', master='develop', options=['--ff-only']):
        cmd = [ 'git', 'pull'] + options  + [upstream, master]
        (ret,output) = self.run(cmd)
        if ret : self.logger.error("sync_upstream failed")

    def merge(self, branch, comment='merged branch '):
        if not comment : comment = 'merged branch ' + branch
        self.logger.info("merging-->" + branch + '<<-')
        cmd = [ 'git', 'merge', '-m', '"' + comment  + '"', branch]
        (ret,output) = self.run(cmd)
        if ret : self.logger.error("merge " + branch + "failed")

    def get_local_branches(self):
        cmd = [ 'git', 'branch']
        (ret,output) = self.run(cmd)
        if ret :
            self.logger.error("git branch failed")
            return []
        branches = list()
        for line in io.StringIO(output.decode()):
            if line[0]=='*':
                branches.insert(0,line[2:].strip())
            else:
                branches.append(line[2:].strip())
        self.logger.debug("branches-->"+str(branches)+"<<-")
        return branches

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
    #print("remote_branches-->",str(remote_branches))
    #  print('#########-->' + url)
    #  for b in remote_branches:
    #    print("       -->",b)
    # ------ Construct the regular expression used to evaluate branches
    branchRE = dict()
    for p in branch_selection:
        # branchRE.append('(' + branch + ')')
        #print("----------->"+p+"<----")
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
        logging.getLogger(__name__).info('{0} fetch-->'.format(url), b)

    return fetch_branches

def trasf_match(in_list,in_match='(.*)',out_format='{name}'):
    #not working#logging.getLogger(__name__).info("in_list-->"+str(in_list)+"<<-")
    #not working#logging.getLogger(__name__).info("in_match-->"+str(in_match)+"<<-")
    out=collections.OrderedDict()
    in_RE = re.compile(in_match)
    for entry in in_list:
        match = in_RE.match(entry)
        if match:
            if 0 < len(match.groups()):
                name = match.group(1)
                out[entry] = out_format.format(name=name)
    return(out)



##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This s taken from Spack.
##############################################################################

def mkdirp(*paths):
    """Creates a directory, as well as parent directories if needed."""
    for path in paths:
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno != errno.EEXIST or not os.path.isdir(path):
                    raise e
        elif not os.path.isdir(path):
            raise OSError(errno.EEXIST, "File already exists", path)


def traverse_tree(source_root, dest_root, rel_path='', **kwargs):
    """Traverse two filesystem trees simultaneously.

    Walks the LinkTree directory in pre or post order.  Yields each
    file in the source directory with a matching path from the dest
    directory, along with whether the file is a directory.
    e.g., for this tree::

        root/
          a/
            file1
            file2
          b/
            file3

    When called on dest, this yields::

        ('root',         'dest')
        ('root/a',       'dest/a')
        ('root/a/file1', 'dest/a/file1')
        ('root/a/file2', 'dest/a/file2')
        ('root/b',       'dest/b')
        ('root/b/file3', 'dest/b/file3')

    Keyword Arguments:
        order (str): Whether to do pre- or post-order traversal. Accepted
            values are 'pre' and 'post'
        ignore (str): Predicate indicating which files to ignore
        follow_nonexisting (bool): Whether to descend into directories in
            ``src`` that do not exit in ``dest``. Default is True
        follow_links (bool): Whether to descend into symlinks in ``src``
    """
    follow_nonexisting = kwargs.get('follow_nonexisting', True)
    follow_links = kwargs.get('follow_link', False)

    # Yield in pre or post order?
    order = kwargs.get('order', 'pre')
    if order not in ('pre', 'post'):
        raise ValueError("Order must be 'pre' or 'post'.")

    # List of relative paths to ignore under the src root.
    ignore = kwargs.get('ignore', lambda filename: False)

    # Don't descend into ignored directories
    if ignore(rel_path):
        return

    source_path = os.path.join(source_root, rel_path)
    dest_path = os.path.join(dest_root, rel_path)

    # preorder yields directories before children
    if order == 'pre':
        yield (source_path, dest_path)

    for f in os.listdir(source_path):
        source_child = os.path.join(source_path, f)
        dest_child = os.path.join(dest_path, f)
        rel_child = os.path.join(rel_path, f)

        # Treat as a directory
        if os.path.isdir(source_child) and (
                follow_links or not os.path.islink(source_child)):

            # When follow_nonexisting isn't set, don't descend into dirs
            # in source that do not exist in dest
            if follow_nonexisting or os.path.exists(dest_child):
                tuples = traverse_tree(
                    source_root, dest_root, rel_child, **kwargs)
                for t in tuples:
                    yield t

        # Treat as a file.
        elif not ignore(os.path.join(rel_path, f)):
            yield (source_child, dest_child)

    if order == 'post':
        yield (source_path, dest_path)


class LinkTree(object):
    """Class to create trees of symbolic links from a source directory.

    LinkTree objects are constructed with a source root.  Their
    methods allow you to create and delete trees of symbolic links
    back to the source tree in specific destination directories.
    Trees comprise symlinks only to files; directries are never
    symlinked to, to prevent the source directory from ever being
    modified.

    """

    def __init__(self, source_root, maxdepth=1000):
        if not os.path.exists(source_root):
            raise IOError("No such file or directory: '%s'", source_root)

        self._root = source_root
        self._maxdepth=maxdepth
        self._linklist=[]

    def find_conflict(self, dest_root, **kwargs):
        """Returns the first file in dest that conflicts with src"""
        kwargs['follow_nonexisting'] = False
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if os.path.isdir(src):
                if os.path.exists(dest) and not os.path.isdir(dest):
                    return dest
            elif os.path.exists(dest):
                return dest
        return None

    def toodepth(self,path):
        listpath = os.path.normpath(path).lstrip(os.path.sep).split(os.path.sep)
        print("aaaaaaa:",listpath,listpath.__len__())
        r = (self._maxdepth < listpath.__len__())
        if r  : self._linklist.append(path)
        self._link= (self._maxdepth == listpath.__len__())
        return (r)

    def merge(self, dest_root, link=os.symlink, **kwargs):
        """Link all files in src into dest, creating directories
           if necessary.
           If ignore_conflicts is True, do not break when the target exists but
           rather return a list of files that could not be linked.
           Note that files blocking directories will still cause an error.
        """
        kwargs['order'] = 'pre'
        kwargs['ignore'] = self.toodepth
        ignore_conflicts = kwargs.get("ignore_conflicts", False)
        existing = []
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if os.path.isdir(src):
                if not os.path.exists(dest):
                    if self._link:
                        print("link:",src)
                        link(src, dest)
                    else:
                        mkdirp(dest)
                    continue

                if not os.path.isdir(dest):
                    raise ValueError("File blocks directory: %s" % dest)

                # mark empty directories so they aren't removed on unmerge.
                if not os.listdir(dest):
                    marker = os.path.join(dest, empty_file_name)
                    touch(marker)

            else:
                if os.path.exists(dest):
                    if ignore_conflicts:
                        existing.append(src)
                    else:
                        raise AssertionError("File already exists: %s" % dest)
                else:
                    link(src, dest)
        if ignore_conflicts:
            return existing

def __toodepth(path,len=2):
    listpath = os.path.normpath(path).lstrip(os.path.sep).split(os.path.sep)
    print("bbbb:",listpath,listpath.__len__())
    r = (2 < listpath.__len__())
    return (r)

#################
if __name__ == '__main__':
    print("__file__:" + os.path.realpath(__file__))
    root=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'cache')
    print("root:" + root)
    l = LinkTree(root,maxdepth=2)
    l.merge('/tmp/cache')

