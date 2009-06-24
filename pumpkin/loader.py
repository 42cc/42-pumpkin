# -*- coding: utf-8 -*-
import sys,os

def load_support(filedir):        
    """load support functions (environment, setup/teardown)
    ugly for now
    """
    def emptyfunc():                        #just callable that does nothing
        pass
    #in case that user can provide no env-functions at all, but they should 
    #be called
    funcs = {"before_all":emptyfunc, "setup":emptyfunc,\
    "teardown":emptyfunc, "after_all":emptyfunc}

    if os.path.isdir(filedir+"support/"):
        try:
            import support
            for key in funcs:               #now looking for matched in user-
                if hasattr(support, key):   #provided functions
                    funcs[key] = getattr(support, key)
            del sys.modules['support']      #removing module, because if we
            return funcs                    #run this once again, it will do
                                            #nothing (on import)
        except:
            sys.stderr.write("""Can`t import support
direcroty exists, but is not a python module.
Please check __init__.py inside dir\n""")
    else:
        sys.stderr.write("Warning: Can`t find step_definitions directory\n")
