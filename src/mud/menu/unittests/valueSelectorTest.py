import unittest
from test import asserts
from util import isString, isFunc, isTuple
from ..valueSelector import ValueSelector

class TestValueSelectorInit(unittest.TestCase):

    def setUp( self ):
        pass

    def test_noEmptyMenu( self ):
        asserts( self, ValueSelector, [] , lambda clientId, selectedValue: None )

    def test_menuItemsAreList( self ):
        asserts( self, ValueSelector, 3 , lambda clientId, selectedValue: None )
        asserts( self, ValueSelector, "" , lambda clientId, selectedValue: None )
        ValueSelector( [""], lambda x: x)

    def test_menuItemDescsAreStrings( self ):
        asserts( self, ValueSelector, [(37,0) ] , lambda clientId, selectedValue: None )
        asserts( self, ValueSelector, [(None,0) ] , lambda clientId, selectedValue: None )
        asserts( self, ValueSelector, [(lambda x: x,0) ] , lambda clientId, selectedValue: None )

    def test_menuItemsTuplesOrStrings( self ):
        asserts( self, ValueSelector, [0 ] , lambda clientId, selectedValue: None )
        asserts( self, ValueSelector, ["",("",5),7 ] , lambda clientId, selectedValue: None )

    def test_menuItemsTuplesArePairs( self ):
        asserts( self, ValueSelector, [("",5,5) ] , lambda clientId, selectedValue: None )
        asserts( self, ValueSelector, ["foo", ("",3,8) ] , lambda clientId, selectedValue: None )

    def test_selectionCallbackIsFunc( self ):
        asserts( self, ValueSelector, [""] , 0 )
        asserts( self, ValueSelector, [""] , None )
        ValueSelector( [""], lambda x: x )

    def test_invalidSelectionCallbackIsFunc( self ):
        asserts( self, ValueSelector, [""] , lambda x: x, 0 )
        asserts( self, ValueSelector, [""] , lambda x: x, "foo" )
        ValueSelector( [""], lambda x: x, lambda x: x )
        
    def test_alphabeticOptionsIsBool( self ):
        asserts( self, ValueSelector, [""] , lambda x: x, lambda x:x, 0 )
        ValueSelector( [""], lambda x: x, lambda x: x, True )

class TestValueSelectorGenerators(unittest.TestCase):

    def setUp( self ):
        self.menu1 = ValueSelector( [("one", 1)], lambda x:x)
        self.menu2 = ValueSelector( [("one", 1),
                                    ("foo", "bob")],
                                    lambda x:x)
        self.menu5 = ValueSelector( [("one", 1),
                                    ("ne", 5),
                                    ("o", ""),
                                    ("onsde", 1),
                                    ("jim", None)],
                                    lambda x:x)

    def test_promptGenerates( self ):
        self.assert_( isString( self.menu1.prompt ) )
        self.assert_( isString( self.menu2.prompt ) )
        self.assert_( isString( self.menu5.prompt ) )

    def test_menuGenerates( self ):
        self.assert_( isString( self.menu1.menu ) )
        self.assert_( isString( self.menu2.menu ) )
        self.assert_( isString( self.menu5.menu ) )

    def test_cmdMapGenerates( self ):
        def checkFind( o, s ):
            self.assert_( isTuple( o.cmdMap.find(s) ) )
            self.assert_( isFunc( o.cmdMap.find(s)[0] ) )
        checkFind( self.menu1, "1" )
        checkFind( self.menu2, "2" )
        checkFind( self.menu5, "5" )

