# -*- coding: utf-8 -*-
"""pumpkin main module, which runs everything"""
import sys
import os
from parser import parse
from pukorators import table
from runner import run
from loader import load_support, load_definitions
def process(filename):
    """take input file and run it"""
    feature_text = file(filename).read()
    feature = parse(feature_text)
    filedir = os.path.dirname(filename)
    sys.path.append(filedir)
    env_funcs = load_support(filedir)
    load_definitions(filedir)
    run(feature, table, env_funcs)

if len(sys.argv) < 2:
    sys.stderr.write("no file specified\n")
else:
    for fname in sys.argv[1:]:
        process(fname)
