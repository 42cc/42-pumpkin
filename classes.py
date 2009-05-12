# -*- coding: utf-8 -*-
"""
    pumpkin classes
"""


class PNode(object):
    '''class for pumpkin tree-like data'''

    def __init__(self, desc, data=None, parrent=None):
        self.data = data
        self.parrent = parrent
        self.desc = desc
        self.children = []

    def add_child(self, child):
        '''function for adding child elements. Nodes or steps'''
        self.children.append(child)
        child.parrent = self


class PStep(object):
    """step rules
    variants:
        0 = given
        1 = when
        2 = then
    """

    def __init__(self, variant, data, parrent=None):
        if variant > 3:
            raise Exception, "wrong type of step: %s" % variant
        self.parrent = parrent
        self.data = data
        self.variant = variant

    def __str__(self):
        return str(self.data)
