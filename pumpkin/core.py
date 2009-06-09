# -*- coding: utf-8 -*-
"""pumpkin module, that works with files"""
import os
import sys
from parser import parse
from pukorators import table
from runner import run

def readfile(filename):        
    """
    read a file and return text from it
    """
    ft_text = ""
    ft_file = file(filename)
    for line in ft_file.readlines():
        ft_text += line
    return ft_text


def find_and_import(filename):
    """find step_definitions file and import it, if exists"""
    filedir = os.path.dirname(filename)
    moduledir = os.path.join(filedir,'step_definitions/')
    modulename = filename.split("/")[-1].split(".")[-2]  #yea, scary. Finding
                #the last element of the path, and cutting out file-extension
    if os.path.isdir(moduledir):
        sys.path.append(moduledir)
        try:
            __import__(str(modulename))
        except:
            sys.stderr.write("No matching definitions file for Feature: %s\n" % modulename)
    else:
        sys.stderr.write("Can`t find step_definitions directory\n")




