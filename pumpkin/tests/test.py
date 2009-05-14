# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
from pumpkin import parser
    
def test_empty_text():
    text = ""
    returnfeature = parser.parse(text)
    assert(returnfeature.description == text)

