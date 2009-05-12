# -*- coding: utf-8 -*-
"""
    Parser
    Pumpkin core module for now

    IMPORTANT:
    For now parser works only with files indented with tabs(\t),
    not with four spaces.
    will fix that later if needed

"""
from classes import PNode, PStep


def processfile(fname):
    '''Read file.'''
    f = file(fname)
    pumpki = PNode(fname)
    seekforwhat = ['feature']
    for line in f.readlines():
        if 'feature' in seekforwhat:
            if line.startswith("Feature:"):
                feature = PNode(line[9:])
                pumpki.add_child(feature)
                seekforwhat = ['fdata']
                continue
            else:
                if not 'scenario' in seekforwhat:
                    raise Exception, "no Feature defined"
        elif seekforwhat[0] == "fdata":
            if line.startswith("\tIn order") \
                or line.startswith("\tAs") \
                or line.startswith("\tI want"):
                if not feature.data:
                    feature.data = []
                    if feature.desc == None:
                        raise Exception, "no Feature defined"
                feature.data.append(line)
                if len(feature.data) == 3:
                    seekforwhat = ['scenario']
                continue

        if 'scenario' in seekforwhat:
            if line.startswith("\tScenario:"):
                scenario = PNode(line[11:])
                feature.add_child(scenario)
                seekforwhat = ['schildren']
                continue
            #else:
                #if not 'feature' in seekforwhat:
                    #raise Exception, "no valid Scenarios found %s" % line

        elif seekforwhat[0] == 'schildren':
            if line.startswith("\t\tGiven"):
                given = PStep(0, line)
                scenario.add_child(given)
                continue
            elif line.startswith("\t\tWhen"):
                when = PStep(1, line)
                scenario.add_child(when)
                continue
            elif line.startswith("\t\tThen"):
                then = PStep(2, line)
                scenario.add_child(then)
                continue
            elif line.startswith("\t\tAnd"):
                andvariant = scenario.children[-1].variant #last element`s type
                andt = PStep(andvariant, line)
                scenario.add_child(andt)
            else:
                seekforwhat = ['scenario', 'feature']
        else:
            pass
    f.close()
    return pumpki
