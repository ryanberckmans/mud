from pydispatch import dispatcher
from util import isInt
import signals

clients = {}

def isClient( clientId ):
    isInt( clientId )
    assert clientId in clients, "core.client.isClient received a clientId that matches no clients (%s)" % clientId


def clientConnectedToServer( clientId ):
    isInt( clientId )
    assert not clientId in clients, "client.newClient received a duplicate clientId (%s)" % clientId
    c = Client( clientId )
    clients[ clientId ] = c
    dispatcher.send( signals.CONNECTED, clientConnectedToServer, clientId )


def clientDisconnectedFromServer( clientId ):
    isClient( clientId )
    dispatcher.send( signals.DISCONNECTED, clientDisconnectedFromServer, clientId )
    del clients[ clientId ]


##################
# Internal #######
##################

class Client:

    def __init__( self, ID ):
        isInt( ID )
        self.ID = ID


