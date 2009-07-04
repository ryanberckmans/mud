import unittest
from test import asserts
from util import isString, isFunc, isTuple
from ..form import Form

class TestFormInit(unittest.TestCase):

    def setUp( self ):
        pass

    def test_noEmptyForm( self ):
        asserts( self, Form, [], lambda x: None )

    def test_menuItemsAreList( self ):
        asserts( self, Form, 3 , lambda x:x )
        asserts( self, Form, "" , lambda x:x )
        Form( [""], lambda x: x)

    def test_menuItemsTuplesOrStrings( self ):
        asserts( self, Form, [0 ] , lambda x:x)
        asserts( self, Form, ["",("",lambda x:x, lambda y:y),7 ] , lambda x:x)

    def test_menuItemDescsAreStrings( self ):
        asserts( self, Form, [(37,lambda x:x, lambda x:x) ] , lambda clientId, selectedValue: None )
        asserts( self, Form, [(None,lambda x:x,lambda x:x) ] , lambda clientId, selectedValue: None )
        asserts( self, Form, [(lambda x: x,lambda x:x,lambda x:x) ] , lambda clientId, selectedValue: None )

    def test_menuItemSelectedFuncIsFunc( self ):
        asserts( self, Form, [("",37, lambda x:x) ] , lambda clientId, selectedValue: None )
        asserts( self, Form, [("","",lambda x:x) ] , lambda clientId, selectedValue: None )

    def test_menuItemValueDescFuncIsFunc( self ):
        asserts( self, Form, [("", lambda x:x,37) ] , lambda clientId, selectedValue: None )
        asserts( self, Form, [("", lambda x:x,"") ] , lambda clientId, selectedValue: None )

    def test_submitCallbackIsFunc( self ):
        asserts( self, Form, [("", lambda x:x,lambda x:x) ] , 5 )
        asserts( self, Form, [("", lambda x:x,lambda x:x) ] , None )
        asserts( self, Form, [("", lambda x:x,lambda x:x) ] , "")

    def test_invalidSelectionCallbackIsFuncOrNone( self ):
        asserts( self, Form, [("", lambda x:x,lambda x:x) ] , lambda x:x, 0 )
        asserts( self, Form, [("", lambda x:x,lambda x:x) ] , lambda x:x, "" )
        Form( [""], lambda x: x, lambda x: x)
        Form( [""], lambda x: x, None)

    def test_alphabeticOptionsIsBool( self ):
        asserts( self, Form, [""] , lambda x: x, lambda x:x, 0 )
        Form( [""], lambda x: x, lambda x: x, True )



        

