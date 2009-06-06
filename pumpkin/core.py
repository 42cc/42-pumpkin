# -*- coding: utf-8 -*-
"""pumpkin core module, which runs everything"""
import os
import sys
from parser import parse
from pukorators import table
from runner import run
#from sys.argv should take the filename
#may be good to take abspath from it
#and also sys.path manipulations
#also filename is made of "filename.feature"
#but step.defs are imported as "filename.py"

def readfile(filename):        
    """
    read a file and return text from it
    """
    ft_text = ""
    ft_file = file(filename)
    for line in ft_file.readlines():
        ft_text += line
    return ft_text

#then parser takes that file and returns feature

def find_and_import(filename):
    modulename = filename.split("/")[-1].split(".")[-2]
    if os.path.isdir("./step_definitions/"):
        sys.path.append("./step_definitions/")
        __import__(str(modulename))


#feature = parse(readfile(filename))
#run(feature,table)

