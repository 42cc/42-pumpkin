# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
from pumpkin import parser
    
def test_empty():
    """parse with empty text as parameter"""
    text = ""
    feature = parser.parse(text)
    assert feature.description == None

def test_some_text():
    """parse with some text, Not the feature definition"""
    text = "blablabla"
    feature = parser.parse(text)
    assert feature.description == None

def test_right():
    """parse valid feature definition"""
    text = """Feature: Testing"""
    feature = parser.parse(text)
    assert feature.description == text
