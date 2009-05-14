# -*- coding: utf-8 -*-
class feature(object):
    def __init__(self, description):
        self.description = description


def parse(text):
    ft = feature(text)
    return ft
