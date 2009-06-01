# -*- coding: utf-8 -*-
import re
def make_mtable(feature, table):        
    """
    make matches of feature-definitions and regexp-func
    table returned from pukorators
    """
    mtable = {}
    for regexp in table:
        #print "regexp " + regexp
        for scenario in feature.scenarios:
            for step_def in scenario.steps:
                #print "step" + strip_statements(step_def)
                if re.match(regexp, strip_statements(step_def)):
                    mtable.update({step_def:table[regexp]})
    #print mtable
    return mtable

def run_tests(mtable):
    """run the tests provided by table of matches"""
    for step in mtable:
        func =  mtable[step]
        func()


def strip_statements(line):
    if line.startswith("Given"):
        line = line[len("Given"):].lstrip()
    elif line.startswith("When"):
        line = line[len("When"):].lstrip()
    elif line.startswith("Then"):
        line = line[len("Then"):].lstrip()
    return line
