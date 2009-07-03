import unittest
from util import isString
from test import asserts
from .. import prompt

class TestPromptObject(unittest.TestCase):

    def setUp(self):
        self.prompt = prompt._Prompt( 0 )

    def test_promptEmptyReturnsEpsilon( self ):
        self.assert_( isString( self.prompt.prompt( None )) )

    def test_promptPushPersists( self ):
        self.prompt.pushPrompt( lambda x: "bob" )
        self.assert_( self.prompt.prompt( None ) == "bob" )

    def test_promptPassesData( self ):
        self.prompt.pushPrompt( lambda x: x )
        self.assert_( self.prompt.prompt( "jim" ) == "jim" )

    def test_promptPushPopIdempotent( self ):
        self.prompt.pushPrompt( lambda x: "bob" )
        self.prompt.popPrompt()
        self.assert_( isString( self.prompt.prompt( None )) )
        self.prompt.pushPrompt( lambda x: x )
        self.prompt.pushPrompt( lambda x: "jim" )
        self.prompt.popPrompt()
        self.assert_( self.prompt.prompt( "fred" ) == "fred" )

    def test_promptPushPopNWorks( self ):
        self.prompt.pushPrompt( lambda x: "bob" )
        self.prompt.pushPrompt( lambda x: "bob" )
        self.prompt.popPrompt( 2 )
        self.assert_( isString( self.prompt.prompt( None )) )

    def test_promptPopNPositive( self ):
        asserts( self, self.prompt.popPrompt, -1 )
        asserts( self, self.prompt.popPrompt, 0 )

    def test_promptPushRequiresFunc( self ):
        asserts( self, self.prompt.pushPrompt, 0 )
        asserts( self, self.prompt.pushPrompt, None )
        self.prompt.pushPrompt( lambda x: x )

    def test_promptPopRequiresInt( self ):
        asserts( self, self.prompt.popPrompt, "foo" )
        asserts( self, self.prompt.popPrompt, None )
        self.prompt.popPrompt( 5 )


class TestPromptModule(unittest.TestCase):

    def setUp(self):
        reload(prompt)

    def test_promptClientIsInt( self ):
        asserts( self, prompt.prompt, "foo", None )

    def test_promptClientExists( self ):
        asserts( self, prompt.prompt, 5, None )
        prompt.tracker.addClient( 8 )
        prompt.prompt( 8, None )

    def test_pushClientIsInt( self ):
        asserts( self, prompt.pushPrompt, "foo", lambda x: x )

    def test_pushClientExists( self ):
        asserts( self, prompt.pushPrompt, 5, lambda x: x )
        prompt.tracker.addClient( 8 )
        prompt.pushPrompt( 8, lambda x: x )

    def test_popClientIsInt( self ):
        asserts( self, prompt.popPrompt, "foo", 5 )

    def test_popClientExists( self ):
        asserts( self, prompt.pushPrompt, 5, 2 )
        prompt.tracker.addClient( 8 )
        prompt.popPrompt( 8, 7 )
