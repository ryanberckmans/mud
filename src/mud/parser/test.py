#!/usr/bin/env python

def loadTestModules():
    import os
    import unittests

    print dir(unittests)
    print unittests.__path__

    modules = []

    for f in os.listdir(os.path.abspath(unittests.__path__[0])):
        if ext == '.py': # Important, ignore .pyc/other files.
            print 'imported module: %s' % (module_name)
            module = __import__(module_name)
            modules.append(module)

    return modules


if __name__ == '__main__':
    import unittest

    print "\nLOADING TESTS...\n"

    modules = loadTestModules()
    
    for module in modules:
        for name in dir(module):
            obj = getattr(module, name)
            if inspect.isclass(obj):
                all_tests.append( unittest.TestLoader().loadTestsFromTestCase(obj))
                print "loaded test: ", obj

    print "\nRUNNING TESTS...\n"

    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(all_tests))
    

