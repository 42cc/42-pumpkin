# -*- coding: utf-8 -*-
import sys


class feature(object):
    def __init__(self,name=None, description=None):
        self.description = description
        self.name = name

   

def parse(text):
    """process text marked up with Gherkin"""

    STATE = "feature"
    ft = None
    for line in text.split("\n"):
        if STATE == "feature":
            ft = create_feature(line)
            print "feature created, name (%s)" % ft.name
            STATE = "f.description"
        elif STATE == "f.description":
            if line.startswith("    "):
                ft = add_description(ft,line.strip())
                print "description!"
        else:
            print "dunno"
    print ft.description
    return ft


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

