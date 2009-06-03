# -*- coding: utf-8 -*-
table = {}
import sys

def given(regexp):
    def _dec(function):
        def wrapper(*args,**kwargs):
            try:
                function(*args,**kwargs)
            except:
                sys.stderr.write("%s failed" % function.__name__)
                print sys.exc_info()[1]
            else:
                print "%s done" % function.__name__
        wrapper.__name__ = function.__name__
        wrapper.__doc__ = function.__doc__
        wrapper.__dict__.update(function.__dict__)
        table.update({regexp:wrapper})
        return wrapper
    return _dec

then = given
when = given
