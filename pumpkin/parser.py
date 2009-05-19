# -*- coding: utf-8 -*-
import sys


class scenario(object):
    def __init__(self,name=None):
        self.name = name
        self.steps = []

class feature(object):
    def __init__(self,name=None, description=None):
        self.description = description
        self.name = name
        self.scenarios = []

   

def parse(text):
    """process text marked up with Gherkin"""

    STATE = "feature"
    ft = None
    text = indent_style(text)
    for line in text:
        if STATE == "feature":
            ft = create_feature(line)
            STATE = "f.description"
        elif STATE == "f.description":
            if line.startswith("    "):
                ft = add_description(ft,line.strip())
            if line.strip() == "":
                STATE = "scenario"
        elif STATE == "scenario":
            if line.strip() == "":
                sys.stderr.write("Warning:Extra empty lines after feature definition")
                continue
            elif line.startswith("    "):
                ft = create_scenario(ft,line.strip())
                STATE = "step"
        elif STATE == "step":
            if line.strip() == "":
                pass
            elif line.startswith("        "):
                ft = add_step(ft,line.strip())
        else:
            print "dunno"
    return ft

def indent_style(text):
    """
    identify tab-style of the given text
    single space, double-space,four-space, tabs, or something else
    """
    import re
    lines = text.split("\n")
    tabsymbol = ""
    if len(lines) > 1:
        for symbol in lines[1]:
            if re.match('\s',symbol):
                tabsymbol += symbol
            else:
                break
        print "("+tabsymbol+")"
        indsymbol = "    "
        newlines = []
        for line in lines:
            line = re.sub('^'+tabsymbol,indsymbol,line)
            line = re.sub('^'+indsymbol+tabsymbol,indsymbol+indsymbol,line)
            newlines.append(line)
        print newlines
        return newlines
    else:
        return lines


def create_feature(line):
    """parse line of text and create feature"""
    if line.startswith("Feature:") :
        name = line[len("Feature:"):].strip()
        ft = feature(name)
    else:
        ft = feature()
        sys.stderr.write("wrong definition of feature on line: \n%s\n" % line)
    return ft

def add_description(feature,line):
    """parse line for description definition"""
    if line.startswith("In order") \
        or line.startswith("As") \
        or line.startswith("I want"):
            if feature.description == None:
                feature.description = []
            feature.description.append(line.strip())
    return feature

def create_scenario(feature,line):
    if line.startswith("Scenario:"):
        sc = scenario(line[len("Scenario:"):].strip())
        feature.scenarios.append(sc)
    return feature



def add_step(feature,line):
    if line.startswith("Given") \
        or line.startswith("When") \
        or line.startswith("Then"):
        feature.scenarios[-1].steps.append(line)
    return feature
