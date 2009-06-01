# -*- coding: utf-8 -*-
table = {}

def given(regexp):
    def _dec(function):
        table.update({regexp:function})
        return function
    return _dec

then = given
when = given
