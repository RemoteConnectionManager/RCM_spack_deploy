# -*- coding: utf-8 -*-
import re
import string

class mytemplate(string.Template):
    def __init__(self,s=''):
        string.Template.__init__(self,s)
        rr="""
         \@(?:
          (?P<escaped>\@) |   # Escape sequence of two delimiters
          (?P<named>[_a-z][_a-z0-9]*)      |   # delimiter and a Python identifier
          \{(?P<braced>[_\.\-a-z][_\.\-a-z0-9]*)\}   |   # delimiter and a braced identifier
          (?P<invalid>\@)              # Other ill-formed delimiter exprs
         )
        """
        self.pattern=re.compile(rr, re.VERBOSE | re.IGNORECASE)
        self.delimiter='@'

    def templ_match(self,s=''):
        m=self.pattern.search(s)
        return m

if __name__ == '__main__':

    d=dict()
    d['PKG_WORK_DIR']="${BA_PKG_WORK_DIR}"
    d["general.download"]="http://www.my.url/pippo.tar.gz"
    d["DOWNLOAD_URL"]="$DOWNLOAD_URL"
    d["PKG_SOURCE_DIR"]="${BA_PKG_SOURCE_DIR}"
    download="""
     -- @@--{pp.qq} -- aa@uu.pp @dddd@
     cd @{PKG_WORK_DIR}
     file=`python -c "import os; import sys;  print os.path.basename(sys.argv[1])" @DOWNLOAD_URL`
     if ! test -f ${file} ; then
       wget @{general.download}
     fi
     mkdir @{PKG_SOURCE_DIR}
     tar -xvzf  ${file} --strip-components=1 -C @{PKG_SOURCE_DIR}


    """
    r= mytemplate().pattern
    print r.pattern
    dd=dict()
    for i in d:
      dd[i]=d[i]
      mi=r.search(download)  
      if mi :
        print "matched input at pos ",mi.start()
        t=mytemplate(download)
        out=t.safe_substitute(dd)
        print out  
        mo=r.search(out)  
        if mo :
            print "matched output at pos ",mo.start()
            print mo.groupdict()
