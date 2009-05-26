# -*- coding: utf-8 -*-
#import pukorators #pumpkin decorators ;)
from pukorators import given

def importCode(code, name):
    """ code can be any object containing code -- string,
    file object, or compiled code object. Returns a new module object initialized by dynamically importing the given code and optionally adds it  to sys.modules under the given name.
    """
    import imp
    module = imp.new_module(name)
    exec code in module.__dict__
    return module

def makeCode(text):
    """function that takes pumpkin`s step definitions
    and converts it to a normal python code (adding imports, global vars, etc)
    """
    head = """\
# -*- coding: utf-8 -*-
from pukorators import given
def run(feature):
"""
    ntext = ""
    funcs = ""
    for line in text.split("\n"):               #adding tabs before lines
        nline = "    " + line + "\n"            #because they are iside def()
        if line.startswith("def"):              #finding all "def" statements
            funcs += "    "+line.strip()[4:-1]  #and putting them to the end
        ntext += nline                          #to be able to run them
    ntext += funcs
    code = head + ntext                         #joining definitions code and header
    return code
    
# DRAFTS!!!!
def run(feature, code):
    defs = importCode(code, "defs")
    defs.run(feature)
    pass

def cutstatements(line):
    if line.startswith("Given"):
        line = line[len("Given"):].lstrip()
    return line
