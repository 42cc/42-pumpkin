# -*- coding: utf-8 -*-
"""
Pumpkin parser module
parses Gherkin-marked text and returns object
with tree-like structure
"""
import sys


class Feature(object):
    """Feature: Contains test reasons, goals and test scenarios"""

    def __init__(self, name=None, description=None):
        self.description = description
        self.name = name
        self.scenarios = []


class Scenario(object):
    """Scenario: set of steps that define tests behaviour"""

    def __init__(self, name=None):
        self.name = name
        self.steps = []


def parse(text):
    """process text marked up with Gherkin"""

    state = "feature"
    feature = None
    text = text.split('\n')
    indent = indent_style(text)
    for line in text:
        if state == "feature":
            feature = create_feature(line)
            state = "f.description"
        elif state == "f.description":
            if line.strip() == "":
                state = "scenario"
            elif line.startswith(indent):
                feature = add_description(feature, line.strip())
        elif state == "scenario":
            if line.startswith(indent):
                feature = create_scenario(feature, line.strip())
                state = "step"
        elif state == "step":
            if line.strip() == "":
                state = "scenario"
            elif line.startswith(indent*2):
                feature.scenarios[-1].steps.append(line.strip())
    return feature


def indent_style(text):
    """
    identify tab-style of the given text
    (single space, double-space, four-space, tabs, or something else)
    and convert it to single standart (four-spaces at the moment)

    in future: possibly clean-up text, erase comment & etc
    """
    import re
    if len(text) > 1:
        indent = ""
        for symbol in text[1]:
            if re.match('\s', symbol):
                indent += symbol         #for multi-spaces
            else:
                break
        return indent
    else:
        return ""



def create_feature(line):
    """parse line of text and create feature"""
    if line.startswith("Feature:"):
        name = line[len("Feature:"):].strip()
        feature = Feature(name)
    else:
        feature = Feature()
        sys.stderr.write("wrong definition of feature on line: \n%s\n" % line)
    return feature


def add_description(feature, line):
    """parse line for description definition"""
    if feature.description == None:
        feature.description = []
    feature.description.append(line.strip())
    return feature


def create_scenario(feature, line):
    """create and append scenario to the feature, passed to the func"""
    if line.startswith("Scenario:"):
        scenario = Scenario(line[len("Scenario:"):].strip())
        feature.scenarios.append(scenario)
    return feature
