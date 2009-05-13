# -*- coding: utf-8 -*-
"""tests for pumpkin app"""
import unittest
from pumpkin import parser
class TestPumpkin(unittest.TestCase):
    
    def testEmptyText(self):
        text = ""
        returnfeature = parser.parse(text)
        self.assertEqual(returnfeature.description, text)

