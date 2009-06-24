import sys, os
from parser import parse
from pukorators import *
from runner import run
from loader import load_support
def process(filename):
    feature_text = file(filename).read()
    feature = parse(feature_text)
    filedir = os.path.dirname(filename)
    sys.path.append(filedir)
    env_funcs = load_support(filedir)
    if os.path.isdir(filedir+"/step_definitions"):
        try:
            import step_definitions
        except:
            sys.stderr.write("""Can`t import step_definitions
direcroty exists, but is not a python module.
Please check __init__.py inside dir\n""")
            sys.stderr.write(str(sys.exc_info()[1]))
    else:
        sys.stderr.write("Warning: Can`t find step_definitions directory\n")
    run(feature, table, env_funcs)

if len(sys.argv) < 2:
    sys.stderr.write("no file specified\n")
else:
    for filename in sys.argv[1:]:
        process(filename)
