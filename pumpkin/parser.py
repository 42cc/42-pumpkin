# -*- coding: utf-8 -*-
import sys


class feature(object):
    def __init__(self,name=None, description=[]):
        self.description = description
        self.name = name



def parse(text):
    """process text marked up with Gherkin"""
    ft = None
    for line in text.split("\n"):
        if ft == None:
            ft = create_feature(line)
        elif not ft == None:
            ft.description.append(line.strip())
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
