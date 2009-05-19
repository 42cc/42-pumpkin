# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
from pumpkin import parser
import sys
STDERR = None   

def setup():
    sys.path.append("/home/meako/documents/Navch/dyplom/42-pumpkin/lib/tddspry/general")
    from mock import Mock
    class mockstderr(Mock):
        """mocking sys.stderr"""
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
    feature = None
    text = None

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
    text = \
"""\
Feature: Testing feature
    In order to test software
    As a developer
    I want to use nice tools\
"""
    feature = parser.parse(text)
    assert feature.name == "Testing feature"
    assert feature.description[0] == "In order to test software"
    assert feature.description[1] == "As a developer"
    assert feature.description[2] == "I want to use nice tools"

def test_empty_line():
    """testing empty line processing, after the feature definition"""
    text = \
"""\
Feature: Testing feature2
    In order to test software
    As a developer
    I want to use nice tools
    
"""
    feature = parser.parse(text)
    assert feature.name == "Testing feature2"
    assert len(feature.description) == 3

def test_scenario():
    """testing that scenario definition not is added to the feature description but treaten as a scenario"""
    text = \
"""\
Feature: Testing feature
    In order to test software
    As a developer
    I want to use nice tools
    
    Scenario: Test_blue_sky\
"""
    feature = parser.parse(text)
    assert len(feature.description) == 3
    assert feature.scenarios[0].name == "Test_blue_sky"

def test_scenario_twolines():
    """
    Same as before, but two lines before scenario definition
    autoindent included
    """
    text = \
"""\
Feature: Testing feature
    In order to test software
    As a developer
    I want to use nice tools


    Scenario: Test_blue_sky\
"""
    feature = parser.parse(text)
    assert len(feature.description) == 3
    assert feature.scenarios[0].name == "Test_blue_sky"
    err = sys.stderr.read()
    assert err == "Warning:Extra empty lines after feature definition"

def test_one_step():
    """
    test processing of first step (given)
    """
    text = \
"""\
Feature: Testing feature
    In order to test software
    As a developer
    I want to use nice tools
    
    Scenario: Test_blue_sky
        Given I am human\
"""
    feature = parser.parse(text)
    assert feature.scenarios[0].name == "Test_blue_sky"
    assert feature.scenarios[0].steps[0] == "Given I am human"
    
def test_steps():
    """
    test processing of multiple steps 
    """
    text = \
"""\
Feature: Testing feature
    In order to test software
    As a developer
    I want to use nice tools
    
    Scenario: Test_blue_sky
        Given I am human
        When I look at the sky
        Then I see that it`s blue\
"""
    feature = parser.parse(text)
    assert feature.scenarios[0].name == "Test_blue_sky"
    assert feature.scenarios[0].steps[0] == "Given I am human"
    assert feature.scenarios[0].steps[1] == "When I look at the sky"
    assert feature.scenarios[0].steps[2] == "Then I see that it`s blue"



