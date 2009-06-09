import sys
from parser import parse
from pukorators import *
from runner import run
from core import find_and_import

def process(filename):
    feature_text = file(filename).read()
    feature = parse(feature_text)
    find_and_import(filename)
    run(feature,table)

if len(sys.argv) < 2:
    sys.stderr.write("no file specified\n")
else:
    for filename in sys.argv[1:]:
        process(filename)
