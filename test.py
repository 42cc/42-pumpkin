# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
import unittest
import os
from pumpkin import processfile
from classes import *


DATA = [1, 2, 3]
DESCRIPTION = "im testing you"
TESTNODE = PNode(DESCRIPTION, DATA)


class TestClasses(unittest.TestCase):
    '''test pumpkin classes'''

    def testNodeCreation(self):
        '''just creating and testing node (parrent)'''
        self.assertEqual(TESTNODE.desc, DESCRIPTION)
        self.assertEqual(TESTNODE.data, DATA)

    def testChild(self):
        '''adding a child to the parrent node'''
        childnode = PNode(DESCRIPTION, DATA)
        TESTNODE.add_child(childnode)
        self.assertEqual(TESTNODE.children[0].desc, DESCRIPTION)
        self.assertEqual(TESTNODE.children[0], childnode)
        self.assertEqual(childnode.parrent, TESTNODE)

    def testStep(self):
        '''creating a PumpkinStep - last child of the nodes'''
        tstep = PStep(0, DATA)
        self.assertEqual(tstep.data, DATA)
        self.assertEqual(str(tstep), str(DATA))
        self.assertEqual(tstep.variant, 0)

    def testBadStep(self):
        '''just testing a bad step'''
        self.assertRaises(Exception, PStep, 4, DATA)


class TestPumpkinParser(unittest.TestCase):
    '''testing feature-file parser'''

    def setUp(self):
        '''creating a sample valid feature-file

        IMPORTANT:
        For now parser works only with files indented with tabs(\t),
        not with four spaces.
        will fix that later if needed

        '''
        tfile = """\
Feature: Work
	In order to get Pumpkin working
	As it`s developer
	I want to test it

	Scenario: Give pumpkin some file to process
		Given I Have pumpkin app
		And i have some testing utils
		When I give it a file named first.ftrs
		Then I Should see succesfull output
		And Everything should be fine

	Scenario: Some second scenario
		Given I Have pumpkin
		And i have some testing utils
		When I give it a file named first.ftrs
		Then I Should do nothing
"""
        filee = open("test.ftrs", 'w')
        for line in tfile:
            filee.write(line)
        filee.close()

    def tearDown(self):
        '''removing feature file'''
        os.remove("test.ftrs")
        

    def testOpeningOfFile(self):
        '''just testing that parser works with valid files'''
        processfile("test.ftrs")

    def testNoFile(self):
        '''trying to open unexisting file'''
        self.assertRaises(IOError, processfile, "foo.ftrs")

    def testFileOkNoFeature(self):
        '''modifying feature-file, removing "Feature" statement, 
        to make it invalid'''
        filee = open("test.ftrs", 'r+')
        lines = filee.readlines()
        filee.close()
        lines[0] = "I am not a feature!"
        filee = open("test.ftrs", 'w')
        filee.writelines(lines)
        filee.close()
        self.assertRaises(Exception, processfile, "test.ftrs")

    def testSuccessfullProcessFile(self):
        '''Testing successfull processing of file.
        Examinating data-struct nodes
        to be corresponding to the statements in feature-file'''
        pumpki = processfile("test.ftrs")
        self.assertEqual(pumpki.children[0].desc, \
        "Work\n")
        self.assertEqual(pumpki.children[0].data[0], \
        "\tIn order to get Pumpkin working\n")
        self.assertEqual(pumpki.children[0].data[1], \
        "\tAs it`s developer\n")
        self.assertEqual(pumpki.children[0].data[2], \
        "\tI want to test it\n")
        self.assertEqual(pumpki.children[0].children[0].desc, \
        "Give pumpkin some file to process\n")
        self.assertEqual(pumpki.children[0].children[0].children[0].data, \
        "\t\tGiven I Have pumpkin app\n")
        self.assertEqual(pumpki.children[0].children[0].children[1].data, \
        "\t\tAnd i have some testing utils\n")
        self.assertEqual(pumpki.children[0].children[0].children[1].variant, 0)
        self.assertEqual(pumpki.children[0].children[0].children[2].data, \
        "\t\tWhen I give it a file named first.ftrs\n")
        self.assertEqual(pumpki.children[0].children[0].children[2].variant, 1)
        self.assertEqual(pumpki.children[0].children[0].children[3].data, \
        "\t\tThen I Should see succesfull output\n")
        self.assertEqual(pumpki.children[0].children[0].children[3].variant, 2)
        self.assertEqual(pumpki.children[0].children[0].children[4].data, \
        "\t\tAnd Everything should be fine\n")
        self.assertEqual(pumpki.children[0].children[1].desc, \
        "Some second scenario\n")
        self.assertEqual(pumpki.children[0].children[1].children[0].data, \
        "\t\tGiven I Have pumpkin\n")
        self.assertEqual(pumpki.children[0].children[1].children[3].data, \
        "\t\tThen I Should do nothing\n")
        self.assertEqual(pumpki.children[0].children[1].children[3].variant, 2)


def main():
    '''docstring just for pylint'''
    unittest.main()

if __name__ == '__main__':
    main()
