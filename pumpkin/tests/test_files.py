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
        Given I add 3759 and 3243
        Then result should be 7002
"""
df_text = """\
from pumpkin.pukorators import *
@given(r'I add (?P<num1>\d*) and (?P<num2>\d*)')
def add(num1,num2):
    global RESULTS
    RESULTS = int(num1) + int(num2)

@then(r'result should be (?P<res>\d*)')
def result(res):
    assert int(res) == RESULTS
"""
defdir = "./step_definitions/"


def setup():
    """creatig feature and def. files"""
    ft_file = open("testing.feature", 'w')
    for line in ft_text:
        ft_file.write(line)
    ft_file.close()

    if not os.path.isdir(defdir):
        os.mkdir(defdir)
    df_file = open(defdir+"testing.py", 'w')
    for line in df_text:
        df_file.write(line)
    df_file.close()

def teardown():
    """removing feature-files"""
    os.remove("testing.feature")
    for file in os.listdir(defdir):
        os.remove(defdir+file)
    os.rmdir(defdir)

class TestFileProcessing:
    """test processing of real files"""
        

    def test_featurefile(self):
        """test function that takes filename and returns text from it"""
        filename = "testing.feature"
        text = core.readfile(filename)
        assert text == ft_text

    def test_def_file(self):
        """takes feature-file, and finds it`s definitions to run"""
        filename = "testing.feature"
        core.find_and_import(filename)
        assert table[r'I add (?P<num1>\d*) and (?P<num2>\d*)'].__name__ == "add" 
        assert table['result should be (?P<res>\d*)'].__name__ =="result"

    def test_full_path(self):
        filename = "/home/meako/documents/Navch/dyplom/42-pumpkin/pumpkin/tests/testing.feature"
        text = core.readfile(filename)
        core.find_and_import(filename)
        assert table[r'I add (?P<num1>\d*) and (?P<num2>\d*)'].__name__ == "add" 
        assert table['result should be (?P<res>\d*)'].__name__ =="result"
