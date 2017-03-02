# -*- coding: utf-8 -*-
import os
import sys
import copy
import ConfigParser
import moduleintrospection
import mytemplate

def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance

class FileTracker:
    def __init__(self):
        self.open_files=[]
    def register(self,fname):
        absname=os.path.abspath(fname)
        if os.path.exists(absname) :
            if not absname in self.open_files :
                self.open_files.append(absname)
    def list(self):
        return(self.open_files)
@singleton
class ConfigTracker(FileTracker):
  pass

            
class baseconfig:
    def __init__(self,confdict=dict()):
        self.confdict=confdict
	self.sections=dict()
	self.options=dict()
        self.clean()

    def parse(self,configfile=''):
        config = ConfigParser.RawConfigParser()

        if(not os.path.exists(configfile)):
            print "WARNING missing platform file -->"+configfile
            return(False)
	#print "parsing configfile-->",configfile,' meta_config ',os.path.dirname(configfile)
        ConfigTracker().register(configfile)

        config.read(configfile)
        for s in config.sections():
            for o in config.options(s):
		#print "confdict ",s,o,"-->",config.get(s, o)
                self.confdict[(s,o)]=config.get(s, o)
		self.sections[s]=self.sections.get(s,[])+[o]
		self.options[o]=self.options.get(o,[])+[s]
        self.clean()
        meta=baseconfig(confdict={
              ('meta_config','path') : os.path.dirname(configfile),
              ('meta_config','toppath') : os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
        })

        out=self.template_subst(meta)
        self.confdict.update(out)
    def clean(self):
        self.sections=dict()
	self.options=dict()
        for (s,o) in self.confdict:
	    self.sections[s]=self.sections.get(s,[])+[o]
	    self.options[o]=self.options.get(o,[])+[s]


    def template_subst(self,config,sections=[]):
        if (isinstance(config,baseconfig)):
            out=dict()
            conf_subst=dict()
            for (c_s,c_o) in config.confdict:
                 st=c_s+'.'+c_o
                 conf_subst[st]=config.confdict[(c_s,c_o)]
            for sect in sections:
                opts=config.sections.get(sect,[])
                for o in opts:
                    conf_subst[o]=config.confdict[(sect,o)]
                    #print "using section ->",sect," option:",o," -->",conf_subst[o]
            #print "template_subst with:",conf_subst     
            for (s,o) in self.confdict:
                v= self.confdict[(s,o)]
                t=mytemplate.mytemplate(v)
                tmp_subst=copy.copy(conf_subst)
                opts=config.sections.get(s,[])
                for new_o in opts:
                    #print "using section:",s," substitute  ",new_o," with-->",config.confdict[(s,new_o)]
                    tmp_subst[new_o]=config.confdict[(s,new_o)]
                #print "t.safe_substitute(tmp_subst)"
                #print t
                #print tmp_subst
                out[(s,o)]=t.safe_substitute(tmp_subst)
            return out
        else:
            print "################################warinit passe wrong object#########"
            return self.confdict

    def merge(self,config,sections=[]):
        if (isinstance(config,baseconfig)):
            out_self=self.template_subst(config,sections=sections)
#            print "##########   out_self  ############"
#            print out_self
            out_config=config.template_subst(self,sections=sections)
#            print "##########   out_config  ############"
#            print out_config
            out_self.update(out_config)
            cfg=baseconfig(confdict=out_self)
            out_total=cfg.template_subst(cfg,sections=sections)
            self.confdict.update(out_total)
            self.clean()

class hierconfig(baseconfig):
    def __init__(self,configfile='config.cfg',dirs=['version','name','common'],init_parse=[],default_sections=[],confdict=dict()):
	baseconfig.__init__(self,confdict=confdict)
        self.configfile=configfile
        self.dirs=dirs
        self.default_sections=default_sections
        for i in init_parse:
            self.parse(i,dirs=[])
        
        

    def parse(self,filename=None,dirs=None):
        if  dirs==None: dirs=self.dirs
        if( not filename): filename='.'

	configs=[]
	if os.path.isdir(filename):
	    path=os.path.abspath(filename)
        else:
	    count = 2
	    fname=filename
	    while ( not os.path.exists(fname) ) and ( count > 0 ) :
	        count = count -1
	        fname = os.path.join(os.path.dirname(os.path.dirname(fname)),os.path.basename(fname))
            if(os.path.exists(fname)):
                configs.append(os.path.abspath(fname))
	    path=os.path.abspath(os.path.dirname(filename))
	    
        if(os.path.exists(path)):
	    for d in dirs:
#		print "configs:",configs
#		print "looking for config in -->",path
		filename=os.path.abspath(os.path.join(path,self.configfile))
		if(os.path.exists(filename)): configs.append(filename)
		path=os.path.dirname(path)
	    configs.reverse()
            for filename in configs:
#                print "parsing-->"+os.path.abspath(filename)
                topconfig=baseconfig()
                topconfig.parse(filename)
                self.merge(topconfig,sections=self.default_sections)    
            self.clean()
            out=self.template_subst(self)
            self.confdict.update(out)
    

class moduleconfig(hierconfig):
    def __init__(self,configfile='config.cfg',init_parse=[],default_sections=['template']):
	self.myintrospect=moduleintrospection.myintrospect()
        initial_config=dict()
        initial_config[('template','domain_name')]=''.join(self.myintrospect.sysintro['hostname'].split('.')[1:][0:1])
        author=self.myintrospect.commands.get("svnauthor",None)
        if author: initial_config[('general','author')]=author
	hierconfig.__init__(self,confdict=initial_config,configfile=configfile,init_parse=init_parse,default_sections=default_sections)
        self.trasl={
            ('module','pkg-name'):('general','name'),
            ('module','pkg-version'):('general','version'),
            ('module','required-modules'):('general','depends'),
            ('module','builad-author'):('general','author'),
        }


    def basereplaces(self):
        basereplaces=dict()
        basereplaces['domain_name']=''.join(self.myintrospect.sysintro['hostname'].split('.')[1:][0:1])
         
        out  = "##################################################################\n"
        out += "### This file is automatically generated on ######################\n"
        out += "### hostname: "+self.myintrospect.sysintro['hostname'] +  " python version: "+ self.myintrospect.sysintro['pyver'] +  "  ##########\n"
        out += "### platform: " + self.myintrospect.sysintro['sysplatform'] + " ##\n"
        out += "###################   using following configuration files   ######\n"
        for i in ConfigTracker().list() :
            out += "## "+ i+"\n"

        out += "###################     by following commands   ##################\n"
        out += "##################################################################\n"
        out += self.myintrospect.reproduce_string('#')
        out += "##################################################################\n"
        basereplaces['reproduce_string']=out
        return basereplaces
        
    def module_options(self):
        m_options=dict()
        for o in self.options:
            for s in ['general','module']:
                v=self.confdict.get((s,o),None)        
                if(v): 
                    m_options[o]=v
                    for (ts,to) in self.trasl:
                        if ((s,o) == self.trasl.get((ts,to),None)):
                            #print " found "+ str((s,o))+ " setting ->"+to+" to "+v
                            m_options[to]=v

        return m_options

    def file_replace(self,rep_sections=[]):
	out=dict()
#	sections=['general','module']
	sections=[]
        basereplaces=self.basereplaces()
	for r in rep_sections:
            replaces=basereplaces
            for o in self.options:
                for s in sections+[r]:
                    v=self.confdict.get((s,o),None)        
                    if(v): 
                        replaces[o]=v
            out[r]=replaces

        return out

def preload(pre_list=[]):
    s=moduleintrospection.myintrospect()
    if 0==len(pre_list) :
        pre_list=['unix',s.sysintro['hostname'].split('.')[1:][0:1][0]]
    print "-----------------hostname-----------",s.sysintro['hostname']
    print "-----------------pre_list-----------",pre_list
    templatedir=os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'templates')
    if not os.path.exists(templatedir):
        print "templtedir "+ templatedir + " missing !!!!!!!!!!!!!"
    preload=[]
    for i in pre_list:
        if os.path.exists(i): cfgfile=i
        else: cfgfile=os.path.join(templatedir,i+'.cfg')
        if os.path.exists(cfgfile): 
            preload.append( cfgfile)   
    return preload


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 : conf_file=sys.argv[1]
    else : conf_file=os.path.join('.','config.cfg')
    cfg = moduleconfig(init_parse=preload())
    cfg.parse(conf_file)
    opt=cfg.module_options()

#    for i in ConfigTracker().list() :
#        print "depends on "+ i

    print "------------------- ba create options ---------------------"
    for o in opt:
        s=opt[o].splitlines()
        if len(s) > 1:
            print o+" : "
            for l in s:
                print "    "+l
        else:
            print o+" -->"+opt[o]+"<"
    build=cfg.file_replace(['BUILD_SCRIPT'])
    module=cfg.file_replace(['MODULEFILE'])

    for f in [build,module]:
        for fr in f:
            print "------------------- " + fr + " replacements -------------"
            for r in f[fr]:
                s=f[fr][r].splitlines()
                if len(s) > 1:
                    print r+" : "
                    print "------------------------------------------------------"
                    for l in s:
                        print "    "+l
                    print "------------------------------------------------------"
                    print 
                else:
                    print r+" -->"+f[fr][r]+"<"


