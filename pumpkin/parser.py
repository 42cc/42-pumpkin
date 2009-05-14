# -*- coding: utf-8 -*-
class feature(object):
    def __init__(self,name=None, description=None):
        self.description = description
        self.name = name



def parse(text):
    if "Feature:" in text:
        name = text[9:]
        ft = feature(name)
    else:
        ft = feature()
    return ft
