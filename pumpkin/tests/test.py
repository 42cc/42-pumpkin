# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
import sys
import os
from tddspry.general.mock import Mock
from pumpkin import parser
from pumpkin import runner
from pumpkin.pukorators import *
from helpers import importCode
STDERR = None   


def setup():
    """functions that run before running tests"""

    class Mockstderr(Mock):
        """
        mocking sys.stderr
        warning: method sys.stderr.read() used in tests
        working correctly only with mocked stderr.

        real stderr does not return EOF
        """
        def __init__(self):
            self.text = ""
        def write(self, err):
            self.text = err
        def read(self):
            return self.text
    STDERR = sys.stderr
    sys.stderr = Mockstderr()

def teardown():
    """runs after tests"""
    sys.stderr = STDERR
    code_def = None
    code_defn = None
    table = None
    mtable = None

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
    parse valid feature name (space)
    (one line with space after "Feature:")
    """
    text = """Feature: Testing"""
    feature = parser.parse(text)
    assert feature.name == "Testing"

def test_right_name_nospace():
    """
    parse valid feature name (nospace)
    (one line without space after "Feature:")
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
    """testing that scenario is treaten as a scenario
    and not added to the feature description"""
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


def test_tabstyle_2spaces():
    """
    test gherkin, marked up with 2-space indents
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
    assert feature.description[0] == "In order to test software"
    assert feature.scenarios[0].name == "Test_blue_sky"
    assert feature.scenarios[0].steps[0] == "Given I am human"

def test_tabstyle_tabulations():
    """
    marked up with tabs
    """
    text = \
"""\
Feature: Testing feature
\tIn order to test software
\tAs a developer
\tI want to use nice tools

\tScenario: Test_blue_sky
\t\tGiven I am human
\t\tWhen I look at the sky
\t\tThen I see that it`s blue\
"""
    feature = parser.parse(text)
    assert feature.description[0] == "In order to test software"
    assert feature.scenarios[0].name == "Test_blue_sky"
    assert feature.scenarios[0].steps[0] == "Given I am human"


def test_three_scenarios():
    """
    processing of multiple scenarios 
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
        Then I see that it`s blue

    Scenario: Test_green_grass
        Given I am on the field
        When I sit down
        Then My pants become green because of grass

    Scenario: Test_yello_sand
        Given I am in the sandstorm
        When I jump up
        Then I jump in the sand\
"""
    feature = parser.parse(text)
    #sys.stderr.write("")
    assert feature.scenarios[0].name == "Test_blue_sky"
    assert feature.scenarios[0].steps[2] == "Then I see that it`s blue"
    assert feature.scenarios[1].name == "Test_green_grass"
    assert feature.scenarios[1].steps[0] == "Given I am on the field"
    assert feature.scenarios[1].steps[1] == "When I sit down"
    assert feature.scenarios[1].steps[2] == \
    "Then My pants become green because of grass"
    assert feature.scenarios[2].name == "Test_yello_sand"
    assert feature.scenarios[2].steps[0] == "Given I am in the sandstorm"
    assert feature.scenarios[2].steps[1] == "When I jump up"
    assert feature.scenarios[2].steps[2] == "Then I jump in the sand"


def _test_table_add():
    """
    add decorated snippet of code to table compilance
    """
    code_def = """\
from pumpkin.pukorators import *
@given('I think that 2+2=5')
def amiright():
    assert 2+2 == 5

@then('I think that 2+2=4')
def imright():
    assert 2+2 == 4\
"""
    assert table == {}
    importCode(code_def, "code_defn")
    assert table["I think that 2+2=5"].__name__ == "amiright"
    assert table["I think that 2+2=4"].__name__ == "imright"

def test_matching_functions():
    """
    Simple regular expression without special characters

    test that step definition in table has a matching
    description in features and matches are added to the new table

    """
    code_def = """\
from pumpkin.pukorators import *
@given('I think that 2 plus 2 = 5')
def amiright():
    assert 2+2 == 5
"""

    code_ftr = """\
Feature: Testing feature
    I want to use nice tools

    Scenario: test math
        Given I think that 2 plus 2 = 5\
"""
    feature = parser.parse(code_ftr)
    importCode(code_def, "code_defn")
    mtable = runner.make_mtable(feature, table)
    assert mtable["Given I think that 2 plus 2 = 5"].__name__ == "amiright"
    assert len(mtable) == 1
    importCode("","code_defn")

def test_matching_functions_regexps():
    """
    Using regular expressions & special characters
    test that step definition in table has a matching
    description in features and matches are added to the new table
    """
    code_def = """\
from pumpkin.pukorators import *
@given(r'I think that \d [+] \d = \d')
def amiright_again():
    assert 2 + 2 == 5
"""

    code_ftr = """\
Feature: Testing feature
    I want to use nice tools

    Scenario: test math
        Given I think that 2 + 2 = 5"""

    feature = parser.parse(code_ftr)
    importCode(code_def, "code_defn")
    mtable = runner.make_mtable(feature, table)
    assert mtable["Given I think that 2 + 2 = 5"].__name__ == "amiright_again"
    assert len(mtable) == 1
    
def test_multi_steps():        
    """
    test with few step definitions and code statements

    """

    code_ftr="""\
Feature: Testing feature
    I want to use nice tools

    Scenario: test math
        Given I think that 2 + 2 = 5
        Then I should be wrong
        """

    code_def = """\
from pumpkin.pukorators import *
@given(r'I think that \d [+] \d = \d')
def amiright_again():
    assert 2 + 2 == 5

@then(r'I should be wrong')
def imwrong():
    assert 2 + 2 == 4
"""
    feature = parser.parse(code_ftr)
    importCode(code_def, "code_defn")
    mtable = runner.make_mtable(feature, table)
    assert mtable["Given I think that 2 + 2 = 5"].__name__ == "amiright_again"
    assert mtable["Then I should be wrong"].__name__ == "imwrong"
    assert len(mtable) == 2


def test_multi_wrong():        
    """
    test with some wrong step definitions and code statements

    later - should add user-notification about undefined steps
    """
    code_ftr= """\
Feature: Testing feature
    I want to use nice tools

    Scenario: test math
        Given I think that 2 + 2 = 5
        Then Khavr should buy me a calculator
        """

    code_def = """\
from pumpkin.pukorators import *
@given(r'I think that \d [+] \d = \d')
def amiright_again():
    assert 2 + 2 == 5
"""
    feature = parser.parse(code_ftr)
    importCode(code_def, "code_defn")
    mtable = runner.make_mtable(feature, table)
    assert mtable["Given I think that 2 + 2 = 5"].__name__ == "amiright_again"
    assert len(mtable) == 1


def test_runner():
    """
    test runner with correct functions and scenarios
    """
    code_ftr= """\
Feature: Testing feature
    I want to use nice tools

    Scenario: test math
        Given I think that 2 + 2 = 4
        """

    code_def = """\
from pumpkin.pukorators import *
@given(r'I think that \d [+] \d = \d')
def imright():
    assert 2 + 2 == 4
"""


    feature = parser.parse(code_ftr)
    importCode(code_def, "code_defn")
    mtable = runner.make_mtable(feature, table)
    assert mtable["Given I think that 2 + 2 = 4"].__name__ == "imright"
    assert len(mtable) == 1
    runner.run_tests(mtable)
    
    
def test_runner_fail():
    """
    test runner with failing functions 
    """
    code_ftr= """\
Feature: Testing feature
    I want to use nice tools

    Scenario: test math
        Given I think that 2 + 2 = 5
        """

    code_def = """\
from pumpkin.pukorators import *
@given(r'I think that \d [+] \d = \d')
def amiright():
    assert 2 + 2 == 5
"""


    feature = parser.parse(code_ftr)
    importCode(code_def, "code_defn")
    mtable = runner.make_mtable(feature, table)
    assert mtable["Given I think that 2 + 2 = 5"].__name__ == "amiright"
    assert len(mtable) == 1
    runner.run_tests(mtable)


def _test_matching_params():
    """
    now test for using variables as parameters for decorators
    """
    code_def = """\
from pumpkin.pukorators import *
@given(r'I think that (?P<var1>\d) [+] (?P<var2>\d) = (?P<var3>\d)')
def amiright_again():
    assert var1 + var2 == var3
"""

    code_ftr = """\
Feature: Testing feature
    I want to use nice tools

    Scenario: test math
        Given I think that 2 + 2 = 5"""

    feature = parser.parse(code_ftr)
    importCode(code_def, "code_defn")
    mtable = runner.make_mtable(feature, table)
    assert mtable["Given I think that 2 + 2 = 5"].__name__ == "amiright_again"
    assert len(mtable) == 1
    runner.run_tests(mtable)
