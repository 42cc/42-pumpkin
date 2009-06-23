# -*- coding: utf-8 -*-
import sys,os

def load_support(filedir):        
    """load support functions (environment, setup/teardown)
    ugly for now
    """
    if os.path.isdir(filedir+"support/"):
        try:
            import support
            global before_all
            before_all = support.before_all

            global setup
            setup = support.setup
            
            global teardown
            teardown = support.teardown
            
            global after_all
            after_all = support.after_all
        except:
            sys.stderr.write("""Can`t import support
direcroty exists, but is not a python module.
Please check __init__.py inside dir\n""")
    else:
        sys.stderr.write("Warning: Can`t find step_definitions directory\n")
