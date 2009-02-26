#!/usr/bin/env python

import unittest

from util import import_libs

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
    
