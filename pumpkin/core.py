# -*- coding: utf-8 -*-
"""pumpkin core module, which runs everything"""
import os
import sys
from parser import parse
from pukorators import table
from runner import run
#from sys.argv should take the filename
#may be good to take abspath from it

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
    filedir = os.path.dirname(filename)
    moduledir = os.path.join(filedir,'step_definitions/')
    modulename = filename.split("/")[-1].split(".")[-2]
    if os.path.isdir(moduledir):
        sys.path.append(moduledir)
        __import__(str(modulename))


#feature = parse(readfile(filename))
#run(feature,table)

