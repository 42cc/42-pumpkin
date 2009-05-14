# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
from pumpkin import parser
    
def test_empty_text():
    text = ""
    feature = parser.parse(text)
    assert feature.description == text

