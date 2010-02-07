import unittest

from .. import cmdMap, exceptions


def blank():
    return lambda : "blank function"

def f( cmd ):
    return lambda : cmd

def call( findResult):
    return findResult[0]()


class TestCmdMapNoAbbrevOneTokenCommand(unittest.TestCase):
    # test completely redundant, but CmdMap doesn't support multitoken noabbrev cmds 2010.2.6
    
    def setUp(self):
        self.map = cmdMap.CmdMap()
        self.map.addCmd("cast", f("0"), False)

    def test_sanity(self):
        self.assert_( call(self.map.find("cast")) == "0" )

    def test_noabbrevCharacterMismatchBailsCorrectly(self):
        self.assert_( self.map.find("castd f roomzd")[0] == None) # mistake in 1st token
        self.assert_( self.map.find("qcast")[0] == None) # mistake at begin of 1st
        self.assert_( call(self.map.find("cast hfireball")) == "0") # correct invocation of cast
 
class TestCmdMapNoAbbrev(unittest.TestCase):
    
    def setUp(self):
        self.map = cmdMap.CmdMap()
        self.map.addCmd("cast", f("0"), False)
        self.map.addCmd("cast fireball", f("10"), False)
        self.map.addCmd("cast fireball room", f("20"), False)
        self.map.addCmd("cast fireball rofl", f("30"), False)
        self.map.addCmd("cast fireball roft", f("35"), False)
        self.map.addCmd("cast fireball root", f("40"), False)
        self.map.addCmd("cast fir tree", f("45"), False)
        self.map.addCmd("cast fir roomz", f("50"), False)

    def test_sanity(self):
        self.assert_( call(self.map.find("cast")) == "0" )
        self.assert_( call(self.map.find("cast fireball")) == "10" )
        self.assert_( call(self.map.find("cast fireball room")) == "20" )
        self.assert_( call(self.map.find("cast fireball rofl")) == "30" )
        self.assert_( call(self.map.find("cast fireball roft")) == "35" )
        self.assert_( call(self.map.find("cast fireball root")) == "40" )
        self.assert_( call(self.map.find("cast fir tree")) == "45" )
        self.assert_( call(self.map.find("cast fir roomz")) == "50" )

    def test_noabbrevCharacterMismatchBailsCorrectly(self):
        self.assert_( self.map.find("castd f roomzd")[0] == None) # mistake in 1st token
        self.assert_( call(self.map.find("cast fireballomg roomzd")) == "0") # mistake in 2nd
        self.assert_( call(self.map.find("cast fireball roomz")) == "10") # mistake in 3rd
        self.assert_( self.map.find("qcast")[0] == None) # mistake at begin of 1st
        self.assert_( call(self.map.find("cast hfireball")) == "0") # mistake at begin of 2nd
        self.assert_( call(self.map.find("cast fireball troom")) == "10") # mistake at begin 3rd

class TestCmdMapAbbrev(unittest.TestCase):
    
    def setUp(self):
        self.map = cmdMap.CmdMap()
        self.map.addCmd("cast", f("0"))
        self.map.addCmd("cast fireball", f("10"))
        self.map.addCmd("cast fireball room", f("20"))
        self.map.addCmd("cast fireball rofl", f("30"))
        self.map.addCmd("cast fireball roft", f("35"))
        self.map.addCmd("cast fireball root", f("40"))
        self.map.addCmd("cast fir tree", f("45"))
        self.map.addCmd("cast fir roomz", f("50"))

    def test_sanity(self):
        self.assert_( call(self.map.find("cast")) == "0" )
        self.assert_( call(self.map.find("cast fireball")) == "10" )
        self.assert_( call(self.map.find("cast fireball room")) == "20" )
        self.assert_( call(self.map.find("cast fireball rofl")) == "30" )
        self.assert_( call(self.map.find("cast fireball roft")) == "35" )
        self.assert_( call(self.map.find("cast fireball root")) == "40" )
        self.assert_( call(self.map.find("cast fir tree")) == "45" )
        self.assert_( call(self.map.find("cast fir roomz")) == "50" )

    def test_abbrevSelectsCorrectCommand(self):
        self.assert_( call(self.map.find("cast f")) == "10")
        self.assert_( call(self.map.find("cast f r")) == "20")
        self.assert_( call(self.map.find("cast f rof")) == "30")
        self.assert_( call(self.map.find("cast f roft")) == "35")
        self.assert_( call(self.map.find("cast fir roft")) == "35")
        self.assert_( call(self.map.find("cast fir roomz")) == "50")
        self.assert_( call(self.map.find("cast fir t t")) == "45")
        self.assert_( call(self.map.find("cast f roomzd")) == "10")
        self.assert_( call(self.map.find("cast fg roomz")) == "0")
        

        

class TestCmdMapDefaultCallback(unittest.TestCase):

    def setUp(self):
        self.map = cmdMap.CmdMap( lambda : "default")

    def test_findDefaultCallbackFromEpsilon(self):
        self.assert_( call(self.map.find("")) == "default" )

    def test_findDefaultCallbackFromBasicNoFind(self):
        self.assert_( call(self.map.find("doesntexist")) == "default" )

    def testsysBasicFindWithDefaultCallback(self):
        self.map.addCmd( "abc", f )
        self.assert_( self.map.find("abc") == (f, None))
        self.assert_( call(self.map.find("abcq")) == "default" )
        self.assert_( call(self.map.find("")) == "default" )

    def testsysAllPrefixesFindWithDefaultCallback(self):
        self.map.addCmd( "abc", f )
        self.assert_( self.map.find("a") == (f, None)) 
        self.assert_( self.map.find("ab") == (f, None)) 

    def testsysMultitokenFindWithDefaultCallback(self):
        self.map.addCmd( "cast fireball", f("quaz") )
        self.assert_(self.map.find("cast fireball") != None)
        self.assert_( call(self.map.find("")) == "default" )
        self.assert_( call(self.map.find("casts fiq")) == "default" )
        self.assert_( call(self.map.find("zcast fireballl")) == "default" )
        self.assert_( call(self.map.find("cast fireball")) == "quaz" )

class TestCmdMap(unittest.TestCase):
    
    def setUp(self):
        self.map = cmdMap.CmdMap()

    def testaddCmdCmdMustBeString(self):
        self.assertRaises(AssertionError, self.map.addCmd, None, f("a"))
        self.assertRaises(AssertionError, self.map.addCmd, 17, f("a"))

    def testaddCmdCallbackMustBeFunction(self):
        self.assertRaises(AssertionError, self.map.addCmd, "Jim", None)
        self.assertRaises(AssertionError, self.map.addCmd, "Jim", 17)

    def testaddCmdAllowAbbrevMustBeBool(self):
        self.assertRaises(AssertionError, self.map.addCmd, "jim", blank(), None)
        self.assertRaises(AssertionError, self.map.addCmd, "jim", blank(), 17)

    def testaddCmdReturnsSelf(self):
        self.assert_(self.map == self.map.addCmd("jim", f("a")))

    def testmapCmdMustBeString(self):
        self.assertRaises(AssertionError, self.map.find, None)
        self.assertRaises(AssertionError, self.map.find, 17)

    def testsysEpsilonFindsNothing(self):
        self.assert_(self.map.find("")[0] == None)

    def testsysBasicFind(self):
        self.map.addCmd( "abc", f )
        self.assert_( self.map.find("abc") == (f, None)) 

    def testsysAllPrefixesFind(self):
        self.map.addCmd( "abc", f )
        self.assert_( self.map.find("a") == (f, None)) 
        self.assert_( self.map.find("ab") == (f, None)) 

    def testsysCallbackWorks(self):
        self.map.addCmd( "abc", f("a") )
        self.assert_(self.map.find("abc")[0]() == "a")

    def testsysMultitokenFind(self):
        self.map.addCmd( "cast fireball", f("quaz") )
        self.assert_(self.map.find("cast fireball") != None)

    def testsysAllPrefixesMultitokenFind(self):
        self.map.addCmd( "cast fly", f("a") )
        self.assert_(self.map.find("c fly") != None )
        self.assert_(self.map.find("ca fly") != None )
        self.assert_(self.map.find("cas fly") != None )
        self.assert_(self.map.find("cast f") != None )
        self.assert_(self.map.find("cast fl") != None )
        self.assert_(self.map.find("cas  f") != None )
        self.assert_(self.map.find("cas  fl") != None )
        self.assert_(self.map.find("cas  fly") != None )
        self.assert_(self.map.find("ca  f") != None )
        self.assert_(self.map.find("ca  fl") != None )
        self.assert_(self.map.find("ca  fly") != None )
        self.assert_(self.map.find("c  f") != None )
        self.assert_(self.map.find("c  fl") != None )
        self.assert_(self.map.find("c  fly") != None )

    def testsysOverwriteFind(self):
        self.map.addCmd( "abc", f("first") )
        self.map.addCmd( "abc", f("second") )
        self.assert_(self.map.find("abc")[0]() == "first")

    def testsysLongerFind(self):
        self.map.addCmd( "abc", f("a") )
        self.map.addCmd( "abcd", f("b") )
        self.assert_(self.map.find("abcd")[0]() == "b")

    def testsysGreedyFind(self):
        self.map.addCmd( "abc", f("a") )
        self.map.addCmd( "abc def", f("b") )
        self.assert_(self.map.find("abc def")[0]() == "b")
        
    def testsysNoAllowAbbrevFind(self):
        self.map.addCmd( "abc", f("a"), False )
        self.assert_(self.map.find("a")[0] == None)
        self.assert_(self.map.find("ab")[0] == None)
        self.assert_(self.map.find("abc") != None)

    def testsysNoAllowAbbrevOverwriteFind(self):
        self.map.addCmd( "abc", f("a"), False )
        self.map.addCmd( "abc", f("b"), False )
        self.assert_(self.map.find("a")[0] == None)
        self.assert_(self.map.find("ab")[0] == None)
        self.assert_(self.map.find("abc")[0]() == "a")

    def testsysNoAllowAbbrevOverwriteLongerFind(self):
        self.map.addCmd( "abc", f("a"), False )
        self.map.addCmd( "abcd", f("b"), False )
        self.assert_(self.map.find("a")[0] == None)
        self.assert_(self.map.find("ab")[0] == None)
        self.assert_(self.map.find("abc")[0]() == "a")
        self.assert_(self.map.find("abcd")[0]() == "b")
