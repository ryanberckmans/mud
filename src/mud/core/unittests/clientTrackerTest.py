import unittest
from test import asserts
from .. import clientTracker

def f( clientId ):
    return clientId

class Foo:
    def __init__(self, clientId ):
        pass

class TestInit(unittest.TestCase):

    def setUp(self):
        pass

    def test_initAddFuncIsCallable(self):
        asserts( self, clientTracker.ClientTracker, None)
        asserts( self, clientTracker.ClientTracker, 12)
        self.assert_( clientTracker.ClientTracker( lambda x: 5 ).addFunc( None ) == 5 )
        clientTracker.ClientTracker( Foo )

class TestClientAdding(unittest.TestCase):

    def setUp(self):
        self.tracker = clientTracker.ClientTracker( f )

    def test_addClientIsInt(self):
        asserts( self, self.tracker.addClient, None )
        asserts( self, self.tracker.addClient, "foo" )
        self.tracker.addClient( 0 )

    def test_addClientNoDuplicates( self ):
        self.tracker.addClient( 0 )
        asserts( self, self.tracker.addClient, 0 )

    def test_addClientAdds( self ):
        self.tracker.addClient( 1 )
        self.assert_(1 in self.tracker.clients)

    def test_addClientAddFuncCalledWithClientId( self ):
        self.tracker.addClient( 5 )
        self.assert_( self.tracker.clients[ 5 ] == 5 )

class TestClientRemoving(unittest.TestCase):

    def setUp(self):
        self.tracker = clientTracker.ClientTracker( f )

    def test_removeClientIsInt(self):
        asserts( self, self.tracker.removeClient, None )
        asserts( self, self.tracker.removeClient, "foo" )

    def test_removeClientMustExist( self ):
        asserts( self, self.tracker.removeClient, 0 )

    def test_removeClientIsDeleted( self ):
        self.tracker.addClient( 1 )
        self.tracker.removeClient( 1 )
        self.assert_(1 not in self.tracker.clients)
        
class TestIsClient(unittest.TestCase):

    def setUp(self):
        self.tracker = clientTracker.ClientTracker( f )

    def test_isClientIsInt(self):
        asserts( self, self.tracker.isClient, None )
        asserts( self, self.tracker.isClient, "foo" )
        self.tracker.isClient( 0 )

    def test_isClientExists(self):
        self.tracker.addClient( 5 )
        self.assert_( self.tracker.isClient ( 5 ) )
        
    def test_isClientDoesntExist(self):
        self.assert_( not self.tracker.isClient ( 5 ) )

        
    
        
