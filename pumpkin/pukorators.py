# -*- coding: utf-8 -*-
def given(regexp):
    def func_wrapper(func,*args,**kw):
        try:
            result = func(*args, **kw)
        except:
            print "%s failed" % func.__name__
            print sys.exc_info()[1]
            pass
        else:
            print "%s done" % func.__name__
            return result
        finally:
            pass
    return func_wrapper
