from util import isInt, isFunc
import signals

class ClientTracker:

    def __init__(self, addFunc):
        assert callable( addFunc )
        
        self.clients = {}
        self.addFunc = addFunc
        signals.connect( self.addClient, signals.CONNECTED )
        signals.connect( self.removeClient, signals.DISCONNECTED )


    def isClient( self, clientId ):
        assert isInt( clientId )

        return clientId in self.clients

    def addClient( self, clientId ):
        assert isInt( clientId )
        assert clientId not in self.clients

        self.clients[ clientId ] = self.addFunc( clientId )
        
    def removeClient( self, clientId ):
        assert isInt( clientId )
        assert clientId in self.clients

        del self.clients[ clientId ]
        
