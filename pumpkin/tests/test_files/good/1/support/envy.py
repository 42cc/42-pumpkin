# -*- coding: utf-8 -*-
"""Sample env file"""

def before_all():
    return "before"

def after_all():
    return "done"

def setup():
    return 5

def teardown():
    return "teardownd"

