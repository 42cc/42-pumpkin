# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
import sys
import os
from pumpkin import parser
from pumpkin import runner
from pumpkin import core
from pumpkin.pukorators import *
from helpers import importCode, Mockstd
STDERR = None   

ft_text = """\
Feature: Work
In order to get Pumpkin working
As it`s developer
I want to test it

Scenario: Test math
    Given i add 3759 and 3243
    Then result should be 7002
"""
df_text = """\
from pumpkin.pukorators import *
result = None
@given(r'I add (?P<num1\d> and (?P<num2>\d)
def add(num1,num2):
result = num1 + num2

@then('result should be (?P<res>\d)
def result(res):
assert res == result\
"""

def setup():
    ft_file = open("testing.feature", 'w')
    for line in ft_text:
        ft_file.write(line)
    ft_file.close()

    if not os.path.isdir("./step_definitions/"):
        os.mkdir("./step_definitions/")
    df_file = open("./step_definitions/testing.py", 'w')
    for line in df_text:
        df_file.write(line)
    df_file.close()

def teardown():
    '''removing feature file'''
    os.remove("testing.feature")
    os.remove("./step_definitions/testing.py")
    os.rmdir("./step_definitions/")

class TestFileProcessing:
    """test processing of real files"""
        

    def test_featurefile(self):
        """test function that takes filename and returns text from it"""
        filename = "testing.feature"
        text = core.readfile(filename)
        assert text == ft_text

    def _test_def_file(self):
        """takes feature-file, and finds it`s definitions to run"""
        filename = "testing.feature"
        assert table == {} 

    def test_nothing(self):
        pass

