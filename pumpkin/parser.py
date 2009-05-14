# -*- coding: utf-8 -*-
class feature(object):
    def __init__(self, description=None):
        self.description = description


def parse(text):
    if "Feature:" in text:
        ft = feature(text)
    else:
        ft = feature()
    return ft
