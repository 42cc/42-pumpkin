# -*- coding: utf-8 -*-
import re
import sys
def run(feature, table):        
    """
    make matches of feature-definitions and regexp-func
    table returned from pukorators
    """
    print "\nrunning Feature: %s" % feature.name
    for desc in feature.description:
        print "    " + desc
    for scenario in feature.scenarios:
        print "\n    Scenario: " + scenario.name
        for step_def in scenario.steps:
            sys.stdout.write("\t%s\t|\t" % step_def)    #using stduot 
#because we dont want newline at the end
            matched = False
            for regexp in table:
                match = re.match(regexp, strip_statements(step_def))
                if match:
                    matched = True
                    params = match.groups()
                    func = table[regexp]
                    func(*params)
            if not matched:
                print "Pending (no matching function)"
    

def strip_statements(line):
    if line.startswith("Given"):
        line = line[len("Given"):].lstrip()
    elif line.startswith("When"):
        line = line[len("When"):].lstrip()
    elif line.startswith("Then"):
        line = line[len("Then"):].lstrip()
    return line
