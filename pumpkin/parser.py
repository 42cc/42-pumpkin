# -*- coding: utf-8 -*-
import sys

class scenario(object):
    def __init__(self,name=None):
        self.name = name

class feature(object):
    def __init__(self,name=None, description=None):
        self.description = description
        self.name = name
        self.scenarios = []

   

def parse(text):
    """process text marked up with Gherkin"""

    STATE = "feature"
    ft = None
    for line in text.split("\n"):
        if STATE == "feature":
            ft = create_feature(line)
            STATE = "f.description"
        elif STATE == "f.description":
            if line.startswith("    "):
                ft = add_description(ft,line.strip())
            if line.strip() == "":
                STATE = "scenario"
                print "looking for "+STATE
        elif STATE == "scenario":
            print line
            ft = create_scenario(ft,line.strip())
        else:
            print "dunno"
    return ft


def create_feature(line):
    """parse line of text and create feature"""
    print line
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
        print sc.name
    return feature
