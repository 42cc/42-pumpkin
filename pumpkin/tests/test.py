# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
from pumpkin import parser
    
def test_empty_text():
    text = ""
    feature = parser.parse(text)
    assert feature.description == None

def test_some_text():
    text = "blablabla"
    feature = parser.parse(text)
    assert feature.description != text

def test_right_text():
    text = "Feature: Testing"
    feature = parser.parse(text)
    assert feature.description == text
