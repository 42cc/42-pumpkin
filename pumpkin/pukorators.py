# -*- coding: utf-8 -*-
"""
set of decorators used in user-provided functions
Those decorators (actualy one) take one argument: regexp for matching with
string in feature-file
decorated functions are wrapped in try-except and added
to the regexp-func table
"""
table = {}
import sys


def given(regexp):
    """deco body"""

    def _dec(function):
        """taking the fucntion as arg"""

        def wrapper(*args, **kwargs):
            """wrapping func into try-except and adding it to the table"""
            try:
                function(*args, **kwargs)
            except:
                print "%s failed" % function.__name__   #not using sys.stderr
                print sys.exc_info()[1]                 #because it breaks
            else:                                       #output formating when
                print "%s done" % function.__name__     #mixed with prints
        wrapper.__name__ = function.__name__
        wrapper.__doc__ = function.__doc__
        wrapper.__dict__.update(function.__dict__)
        table.update({regexp: wrapper})
        return wrapper
    return _dec

then = given
when = given
