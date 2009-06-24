# -*- coding: utf-8 -*-
"""Env file for test
using sys.stderr only for testing
purposes, because it`s already mocked
"""
import sys

def before_all():
    sys.stderr.write("before")

def after_all():
    sys.stderr.write("after")

def setup():
    sys.stderr.write("setup")

def teardown():
    sys.stderr.write("teardown")
