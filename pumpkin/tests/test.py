# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
from pumpkin import parser
#import nose.plugins.capture as capture
import sys
STDERR = None   

def setup():
    class mockstderr:
      def __init__(self):
        self.fl=""
      def write(self,x):
        self.fl=x
      def read(self):
        return self.fl
    STDERR=sys.stderr
    sys.stderr=mockstderr()

def teardown():
    sys.stderr = STDERR

def test_empty():
    """parse with empty text as parameter"""
    text = ""
    feature = parser.parse(text)
    assert feature.name == None
    err = sys.stderr.read()
    assert err == """wrong definition of feature on line: \
\n%s\n""" % text

def test_some_text():
    """parse with some text, Not the feature definition"""
    text = "blablabla"
    feature = parser.parse(text)
    assert feature.name == None
    err = sys.stderr.read()
    assert err == """wrong definition of feature on line: \
\n%s\n""" % text

def test_right_name_space():
    """
    parse valid feature name (one line)
    (with space after "Feature:")
    """
    text = """Feature: Testing"""
    feature = parser.parse(text)
    assert feature.name == "Testing"

def test_right_name_nospace():
    """
    parse valid feature name (one line)
    (without space after "Feature:")
    """
    text = """Feature:Testing"""
    feature = parser.parse(text)
    assert feature.name == "Testing"

def test_feature_mid():
    """
    what if there is some text before "Feature:" statement
    That`s wrong
    """
    text = """Blablab Feature:Testing"""
    feature = parser.parse(text)
    assert feature.name == None
    err = sys.stderr.read()
    assert err == """wrong definition of feature on line: \
\n%s\n""" % text

def test_full_definition():
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


