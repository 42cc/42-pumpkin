# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
from pumpkin import parser
    
def test_empty():
    """parse with empty text as parameter"""
    text = ""
    feature = parser.parse(text)
    assert feature.name == None

def test_some_text():
    """parse with some text, Not the feature definition"""
    text = "blablabla"
    feature = parser.parse(text)
    assert feature.name == None

def test_right_name_space():
    """parse valid feature name (one line)(with space after "Feature:" """
    text = """Feature: Testing"""
    feature = parser.parse(text)
    assert feature.name == "Testing"

def test_right_name_nospace():
    """parse valid feature name (one line)"""
    text = """Feature:Testing"""
    feature = parser.parse(text)
    assert feature.name == "Testing"

def _test_full_definition():
    """parsing full feature definition"""
    text = """Feature: Testing feature
        As a developer
        In order to test software
        I want to use nice tools"""
    feature = parser.parse(text)
    assert feature.name == "Testing feature"
    assert feature.description[0] == "As a developer"
    assert feature.description[1] == "In order to test software"
    assert feature.description[2] == "I want to use nice tools"


