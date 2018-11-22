import inspect
import types

class top(object):

    def _print_intro(self):
        print("class name",self.__class__.__name__)
        for cls in self.__class__.__bases__:
            print("parent:", cls.__name__)

        methods=[(name,fn) for name,fn in inspect.getmembers(self.__class__)  if callable(getattr(self.__class__, name)) and not name.startswith("__")]
        print("methods:",methods)
        signature=dict()
        for name,fn in methods:
            signature['getargspec'] = inspect.getargspec(fn)
            signature['getfullargspec'] = inspect.getfullargspec(fn)
            #signature=inspect.getargspec(inspect.getmembers(self.__class__)[method_name])
            for m in ['getargspec','getfullargspec']:
                print(m," : ",name," :: ",signature[m])
                for par in signature.get('defaults',dict()) :
                    if(par != 'self'):
                        print("par: ",par, )



        # print("metho")
        # for name,fn in inspect.getmembers(self.__class__, predicate=inspect.ismethod):
        #     print("here", name )
        #     if isinstance(fn, types.MethodType) and name != '__init__':
        #         print("here1", name)
        #         f_args=inspect.getargspec(fn)[0]
        #         #functions[str(name)]=(fn,f_args)
        #         #help+="\n --command="+str(name)
        #         print("method:",name)
        #         for par in f_args :
        #             if(par != 'self'):
        #                 print("par: ",par)
        #                 #parameters[par]= "--"+par
        #                 #help+=" "+parameters[par]+"=<"+par+">"

def decorator(function):

    def inner(self):
        self_type = type(self)
        # self_type is now the class of the instance of the method that this
        # decorator is wrapping
        print('The class attribute docpath is %r' % self_type.docpath)

        # need to pass self through because at the point function is
        # decorated it has not been bound to an instance, and so it is just a
        # normal function which takes self as the first argument.
        function(self)

    return inner


class A(top):
    docpath = "A's docpath"

    #@decorator
    def a_method(self,par1='def_par1'):
        print('a_method')


class B(A):
    docpath = "B's docpath"

    def b_method(self,par0,par2='def_par2',par3='def_par3'):
        print('b_method')
a = A()
a.a_method()

b = B()
b.a_method()
b._print_intro()
