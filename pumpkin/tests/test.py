# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
from pumpkin import parser
class TestPumpkin(object):
    
    def testEmptyText(self):
        text = ""
        returnfeature = parser.parse(text)
        assert(returnfeature.description == text)

