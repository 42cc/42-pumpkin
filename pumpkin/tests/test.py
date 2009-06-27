# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
import sys
import os
from pumpkin import parser
from pumpkin import runner
from pumpkin import loader
from pumpkin.pukorators import *
from helpers import Mockstd
STDERR = None   
sys.argv = ['pumpkin.py']           #Needed for correct import on next line
import pumpkin.pumpkin as pumpkicore   #importing pumpkin executable
testsdir = os.path.abspath(os.path.dirname(__file__))
filedir = os.path.join(testsdir, "test_files/")
featurefile = os.path.join(filedir, "good/1/working.feature")
gooddir = os.path.join(filedir, "good/")
faildir = os.path.join(filedir, "failing/")
defdir = os.path.join(gooddir, "1/step_definitions/")
sys.path.append(defdir)
PATH = sys.path[:]                   #backing up sys.path

class TestParser:
    """pumpkin Parser module takes gherkin-marked text and returns feature obj"""

    def setUp(self):
        """functions that run before running each test"""
        STDERR = sys.stderr
        sys.stderr = Mockstd()

    def tearDown(self):
        """runs after tests"""
        sys.stderr = STDERR

    def test_empty(self):
        """parse with empty text as parameter"""
        text = ""
        feature = parser.parse(text)
        assert feature.name == None
        err = sys.stderr.read()
        assert err == """wrong definition of feature on line: \
\n%s\n""" % text

    def test_some_text(self):
        """parse with some text, Not the feature definition"""
        text = "blablabla"
        feature = parser.parse(text)
        assert feature.name == None
        err = sys.stderr.read()
        assert err == """wrong definition of feature on line: \
\n%s\n""" % text

    def test_right_name_space(self):
        """
        parse valid feature name (space)
        (one line with space after "Feature:")
        """
        text = """Feature: Testing"""
        feature = parser.parse(text)
        assert feature.name == "Testing"

    def test_right_name_nospace(self):
        """
        parse valid feature name (nospace)
        (one line without space after "Feature:")
        """
        text = """Feature:Testing"""
        feature = parser.parse(text)
        assert feature.name == "Testing"

    def test_feature_mid(self):
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

    def test_full_definition(self):
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

    def test_empty_line(self):
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

    def test_scenario(self):
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

    def test_scenario_twolines(self):
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

    def test_one_step(self):
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
        
    def test_steps(self):
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


    def test_tabstyle_2spaces(self):
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

    def test_tabstyle_tabulations(self):
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


    def test_three_scenarios(self):
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
    
    
class TestDecorators:
    """pumpkin decorators (pukorators). Adding their params into regexp-table and
    wrapping functions in try-except statements"""

    def test_table_add(self):
        """
        add decorated snippet of code to table compilance
        """
        
        import table_add
        assert table["I think that 2+2=5"].__name__ == "amiright"
        assert table["I think that 2+2=4"].__name__ == "imright"

class TestRunner:        
    """runner. Runs tests defined in definitions, against feature obj"""

    def setUp(self):
        """functions that run before running each test"""
        STDERR = sys.stderr
        sys.stderr = Mockstd()
        sys.path = PATH[:]

    def tearDown(self):
        """runs after tests"""
        sys.stderr = STDERR
        table = None

  
    def test_matching_params(self):
        """
        now test for using variables as parameters for decorators
        """

        code_ftr = """\
Feature: Testing feature
    I want to use nice tools

    Scenario: test math
        Given I think : 3 + 2 = 5
        When answer is 5, then it sounds "five"\
"""    
        def emptyfunc():
            pass
        funcs = {"before_all":emptyfunc, "setup":emptyfunc,\
        "teardown":emptyfunc, "after_all":emptyfunc}
        feature = parser.parse(code_ftr)
        import match_param
        runner.run(feature, table, funcs)
        assert sys.stderr.read() == ""
        
    def test_with_support(self):
        """
        now with support functions
        """
        code_ftr = """\
Feature: Testing feature
    I want to use nice tools

    Scenario: test math
        Given I think : 3 + 2 = 5
        When answer is 5, then it sounds "five"\
"""
        feature = parser.parse(code_ftr)
        import match_param
        sys.path.append(gooddir+"3")
        env_funcs = loader.load_support(gooddir+"3/")
        sys.path.remove(gooddir+"3")
        runner.run(feature, table, env_funcs)
        assert sys.stderr.read() == "beforesetupteardownafter" #;)

class TestPumpkinModule:
    def setUp(self):
        """functions that run before running each test"""
        sys.stderr = Mockstd()

    def tearDown(self):
        """runs after tests"""
        sys.argv = []
        sys.stderr = None

    def test_nofile(self):
        """test that pumpkin exits properly when no file is specified"""
        sys.argv = ['pumpkin.py']
        reload(pumpkicore)
        assert sys.stderr.read() == "no file specified\n"

    def test_no_defdir(self):
        """feature-file is specified and ok, but no definitions dir"""
        failfile = os.path.join(filedir, "failing/1/fail.feature")
        sys.argv = ['pumpkin.py', failfile]
        reload(pumpkicore)
        assert sys.stderr.read() == "Warning: Can`t find step_definitions directory\n"

    def test_defdir_nomodule(self):
        """definitions dir exists, but not as a python module"""
        failfile = os.path.join(filedir, "failing/2/fail.feature")
        sys.argv = ['pumpkin.py', failfile]
        reload(pumpkicore)
        assert sys.stderr.read().startswith("Can`t import") == True
        
    def test_processing(self):
        """test that when everything is ok, pumpkin works ok"""
        sys.argv = ['pumpkin.py',featurefile]
        reload(pumpkicore)
        assert sys.stderr.read() == ""

class TestLoader():
    """loader module. Loads step_definitions and support (setup/teardown)"""

    def setUp(self):
        sys.stderr = Mockstd()
        #reload(loader)

    def tearDown(self):
        pass

    def test_load_support(self):
        """loading full-featured support file
        with global and local setups/teardowns"""
        sys.path.append(gooddir+"/1/")
        funcs = loader.load_support(gooddir+"/1/")
        assert funcs["before_all"]() == "before"
        assert funcs["setup"]() == 5
        assert funcs["teardown"]() == "teardownd"
        assert funcs["after_all"]() == "done"
        sys.path.remove(gooddir+"/1/")

    def test_bad_support(self):
        """support dir exists, but not a module"""
        sys.path.append(faildir+"/2")
        funcs = loader.load_support(faildir+"/2/")
        assert sys.stderr.read().startswith("Can`t import support")
        sys.path.remove(faildir+"/2")


    def test_not_full_support(self):
        """support only with local setup&teardown"""
        sys.path.append(gooddir+"/2/")
        funcs = loader.load_support(gooddir+"/2/")
        assert funcs["setup"]() == 6
        assert funcs["teardown"]() == "teardownd2"
        assert funcs["after_all"]() == None
        sys.path.remove(gooddir+"/2/")
