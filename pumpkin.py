# -*- coding: utf-8 -*-
"""
    Parser
    Pumpkin core module for now
"""
import sys


def processfile(filename):
	'''Read file.'''
	f = file(filename)
	features = []
    for line in f.readlines():
		line = f.readline()
        if line.startswith("Feature:")
        #*** Create feature data***
        #process next lines for scenarios and steps
	f.close()

    

#parsing command line arguments. 
if len(sys.argv) < 2:
	print 'No action specified.'
	sys.exit()

if sys.argv[1].startswith('--'):
	option = sys.argv[1][2:]
	# fetch sys.argv[1] but without the first two characters
	if option == 'version':
		print 'Version 0.01'
	elif option == 'help':
		print '''\
        Pumpkin - the python clone of Cucumber(ruby)
  --version : Prints the version number
  --help    : Display this help'''
	else:
		print 'Unknown option.'
	sys.exit()
else:
	for filename in sys.argv[1:]:
		processfile(filename)

