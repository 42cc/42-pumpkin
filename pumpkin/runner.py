# -*- coding: utf-8 -*-
"""take everything processed before and run it!"""
import re


def run(feature, table, env_funcs):
    """
    make matches between feature-definitions and regexp-func
    table returned from pukorators
    """
    print "\nrunning Feature: %s" % feature.name
    env_funcs["before_all"]()
    for desc in feature.description:
        print "    " + desc
    for scenario in feature.scenarios:
        print "\n    Scenario: " + scenario.name
        env_funcs["setup"]()
        for step_def in scenario.steps:
            print("\t%s\t|\t" % step_def),    #coma at the end = no newline
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
        env_funcs["teardown"]()
    env_funcs["after_all"]()
