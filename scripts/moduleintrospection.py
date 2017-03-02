# -*- coding: utf-8 -*-
import subprocess
import sys
import platform
import os
import re
import socket

def run(cmd):
    print "running command--->"+cmd 
    args=cmd.split()
    myprocess = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = myprocess.communicate()
    myprocess.wait()
    #print "out-->"+stdout
    #print "err-->"+stderr
    return (stdout,stderr)

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
        (o,e)=run(cmd)
        if not e :
            if not key : key=cmd
            self.commands[key]=o

class myintrospect(commandintrospect):
    def __init__(self):
        
        commandintrospect.__init__(self,['svn --version'])

        self.test('svnversion '+self.sysintro['workdir'],key='svnrevision')
        
        (out,err)=run('svn info '+self.sysintro['workdir'])
        for (cmd,match) in [("svnurl","URL: "),("svnauthor","Last Changed Author: ")]:
            for line in out.splitlines():
	        if match in line:
		    self.commands[cmd] = line[len(match):]
		    break

    def reproduce_string(self,comment=''):
        out = comment+"module load ba\n"
        try:
            revision=int(self.commands['svnrevision'])
        except :
            print "WARNING svn not clean"
            c=re.compile('(^[0-9]*)')
            m=c.match(self.commands['svnrevision'])
            revision=m.groups()[0]
        out +=comment+"svn co "+self.commands['svnurl']+'@'+str(revision)+" my_common_source\n"
        out +=comment+"cd my_common_source\n"
        out +=comment+self.sysintro['pyinterp']+' '+self.sysintro['commandline']+'\n'
        return out

if __name__ == '__main__':
    me=myintrospect()
    for k in me.sysintro:
       print k+' -->'+me.sysintro[k]+'<'
    for k in me.commands:
       print k+' -->'+me.commands[k]+'<'
    
    print me.reproduce_string('#')

