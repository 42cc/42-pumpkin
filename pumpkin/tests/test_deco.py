# -*- coding: utf-8 -*-
"""tests for decorators, introduced in #2""" 
from pumpkin import parser
from pumpkin import definitor

def test_given_decorator():
    text = """Feature: Search
  In order to learn more
  As an information seeker
  I want to find more information
 
  Scenario: Find what I'm looking for
    Given I am on the Google search page
    When I search for "42 coffee cups"
    Then I should see a link to "http://twitter.com/42cc"
"""
    feature = parser.parse(text)    
    step_defs = definitor.define(feature) #convert features to a python source code
    step_defs[0] = """@given("I am on the Google search page")""" #first line of the converted code
    
