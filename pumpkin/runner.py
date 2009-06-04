# -*- coding: utf-8 -*-
import re
def run(feature, table):        
    """
    make matches of feature-definitions and regexp-func
    table returned from pukorators
    """
    for regexp in table:
        #print "regexp " + regexp
        for scenario in feature.scenarios:
            for step_def in scenario.steps:
                #print "step" + strip_statements(step_def)
                if re.match(regexp, strip_statements(step_def)):
                    params = re.match(regexp, strip_statements(step_def)).groups()
                    func = table[regexp]
                    if len(params) > 0:
                        func(*params)
                    else:
                        func()



def strip_statements(line):
    if line.startswith("Given"):
        line = line[len("Given"):].lstrip()
    elif line.startswith("When"):
        line = line[len("When"):].lstrip()
    elif line.startswith("Then"):
        line = line[len("Then"):].lstrip()
    return line
