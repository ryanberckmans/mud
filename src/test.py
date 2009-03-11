#!/usr/bin/env python


def loadTestModules():
    import os
    import mud

    modules = []

    for pkgName in mud.__all__:
        __import__("mud.%s.unittests" % pkgName)
        for f in os.listdir(os.path.abspath("mud/%s/unittests" % pkgName )):
            module, ext = os.path.splitext(f) # Handles no-extension files, etc.      
            if ext == '.py' and module != '__init__': # Important, ignore .pyc/other files.
                print 'imported module: mud.%s.unittests.%s' % (pkgName, module)
                modules.append(__import__("mud.%s.unittests.%s" % (pkgName,module) ) )

    return modules


if __name__ == '__main__':
    import unittest

    print "\nLOADING TESTS...\n"

    modules = loadTestModules()

    tests = []
    
    for module in modules:
        for name in dir(module):
            obj = getattr(module, name)
            if inspect.isclass(obj):
                tests.append( unittest.TestLoader().loadTestsFromTestCase(obj))
                print "loaded test: ", obj

    print "\nRUNNING TESTS...\n"

    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(tests))
    

