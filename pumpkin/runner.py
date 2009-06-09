# -*- coding: utf-8 -*-
import re
import sys
def run(feature, table):        
    """
    make matches between feature-definitions and regexp-func
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
                match = re.search(regexp, step_def)
                if match:
                    matched = True
                    params = match.groups()
                    func = table[regexp]
                    func(*params)
            if not matched:
                print "Pending (no matching function)"
    
