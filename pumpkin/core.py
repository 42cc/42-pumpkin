# -*- coding: utf-8 -*-
"""pumpkin core module, which runs everything"""

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
    if os.path.isdir("./step_definitions/") #file dir+step_defs
        sys.path.append




