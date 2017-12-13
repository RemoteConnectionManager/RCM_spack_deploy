import utils
import os
import logging

#################
if __name__ == '__main__':
    import tempfile
    import shutil

    print("__file__:" + os.path.realpath(__file__))
    #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    #logging.debug('This message should appear on the console')
    #logging.info('So should this')
    #logging.warning('And this, too')
    print("########### "+__name__)
    ll = logging.getLogger('@@'+__name__)
    ll.setLevel(logging.DEBUG)
    for h in ll.handlers :
        h.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s %(name)s[%(filename)s:%(lineno)s ] %(message)s")
        h.setFormatter(formatter)


    for k,v in utils.baseintrospect().sysintro.items() : print("sysintro["+ k +"]=" + v )
    me=utils.myintrospect(tags={'calori': 'ws_mint', 'galileo':'galileo', 'marconi':'marconi', 'eni':'eni' })
    for k,v in me.commands.items() : print("commands["+ k +"]=" + v )
    print("myintrospection:  host->" + me.platform_tag())
    root=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'cache')
    print("root:" + root)
    l = utils.LinkTree(root,maxdepth=2)
    dest=tempfile.mkdtemp()
    l.merge(dest)
    ll.info("Num folders in dest: " + str(len(os.listdir(dest))))
    shutil.rmtree(dest, ignore_errors=True)


    #for h in ll.handlers:
    #    h.setFormatter("[%(filename)s:%(lineno)s - %(funcName)20s() %(asctime)s] %(message)s")
    #    h.setLevel(logging.DEBUG)
    #origin='https://github.com/RemoteConnectionManager/RCM_spack_deploy.git'
    #branches=['master']
    #origin='https://github.com/RemoteConnectionManager/spack.git'
    #branches=['clean/develop']
    for origin,branches in [
        #('https://github.com/RemoteConnectionManager/spack.git',['clean/develop']),
        #('https://github.com/RemoteConnectionManager/RCM_spack_deploy.git',['master'])
                            ] :
        dest=tempfile.mkdtemp()
        ll.info("creating TEMP dir ->" + dest)
        repo=utils.git_repo(dest,logger=ll)
        origin_branches = utils.get_branches(origin, branch_selection=branches)
        repo.init()
        repo.add_remote(origin, name='origin', fetch_branches=origin_branches)
        repo.fetch(name='origin',branches=origin_branches)
        repo.checkout(origin_branches[0])
        ll.info(os.listdir(dest))
        shutil.rmtree(dest, ignore_errors=True)
