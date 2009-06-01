# -*- coding: utf-8 -*-
import re
def make_ctable(feature, table):        
    """
    make comparsion table of feature 
    definitions and regexp-func table returned from pukorators
    """
    ctable = {}
    for regexp in table:
        print "regexp "+regexp
        for scenario in feature.scenarios:
            for step_def in scenario.steps:
                print "step " + strip_statements(step_def)
                if re.match(regexp, strip_statements(step_def)):
                    print "matched"
                    ctable.update({step_def:table[regexp]})
    print ctable
    return ctable

    

def strip_statements(line):
    if line.startswith("Given"):
        line = line[len("Given"):].lstrip()
    elif line.startswith("When"):
        line = line[len("When"):].lstrip()
    elif line.startswith("Then"):
        line = line[len("Then"):].lstrip()
    return line
