# -*- coding: utf-8 -*-
table = {}

def given(regexp):
    def _dec(function):
        def wrapper(*args, **kwargs):
            pass
        wrapper.__name__ = function.__name__
        wrapper.__doc__ = function.__doc__
        wrapper.__dict__.update(function.__dict__)
        table.update({regexp:wrapper})
        return wrapper
    return _dec

then = given
when = given
