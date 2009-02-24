#!/usr/bin/env python

"""
loader.py - From a directory name:

1: append the directory to the sys.path
2: find all modules within that directory
3: import all modules within that directory
4: filter out built in methods from those modules
5: return a list of useable methods from those modules

Allows the user to import a series of python modules without "knowing" anything
about those modules.

Copyright 2005 Jesse Noller <jnoller@gmail.com>

"""

import os, sys, inspect
import unittest

def import_libs(dir):
    """ Imports the libs, returns a list of the libraries. 
    Pass in dir to scan """
    
    library_list = []

    for f in os.listdir(os.path.abspath(dir)):       
        module_name, ext = os.path.splitext(f) # Handles no-extension files, etc.
        if ext == '.py': # Important, ignore .pyc/other files.
            print 'imported test module: %s' % (module_name)
            module = __import__(module_name)
            library_list.append(module)
 
    return library_list


# Our code

if __name__ == '__main__':

    print "\nLOADING TESTS...\n"

    all_tests = []
    
    tests = import_libs("./unittests")

    for module in tests:
        for name in dir(module):
            obj = getattr(module, name)
            if inspect.isclass(obj):
                all_tests.append( unittest.TestLoader().loadTestsFromTestCase(obj))
                print "loaded test: ", obj

    print "\nRUNNING TESTS...\n"

    # Convert the list of tests into a suite
    #mud_suite = unittest.TestSuite(all_tests)
    
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(all_tests))
    
