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
    text = indent_style(text)
    for line in text:
        if state == "feature":
            feature = create_feature(line)
            state = "f.description"
        elif state == "f.description":
            if line.strip() == "":
                state = "scenario"
            elif line.startswith("    "):
                feature = add_description(feature, line.strip())
        elif state == "scenario":
            if line.startswith("    "):
                feature = create_scenario(feature, line.strip())
                state = "step"
        elif state == "step":
            if line.strip() == "":
                state = "scenario"
            elif line.startswith("        "):
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
    lines = text.split("\n")
    if len(lines) > 1:
        indent = ""                      #tabulation actually used in text
        for symbol in lines[1]:
            if re.match('\s', symbol):
                indent += symbol         #for multi-spaces
            else:
                break
        indsymbol = "    "               #indentation symbol that we use
        newlines = []
        for line in lines:
            line = re.sub('^'+indent, indsymbol, line)
            line = re.sub('^'+indsymbol+indent, indsymbol+indsymbol, line)
            newlines.append(line)
        return newlines
    else:
        return lines


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
