import sys, os
from parser import parse
from pukorators import *
from runner import run

def process(filename):
    feature_text = file(filename).read()
    feature = parse(feature_text)
    filedir = os.path.dirname(filename)
    sys.path.append(filedir)
    import step_definitions
    run(feature,table)

if len(sys.argv) < 2:
    sys.stderr.write("no file specified\n")
else:
    for filename in sys.argv[1:]:
        process(filename)
