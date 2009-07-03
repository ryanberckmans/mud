from util import isString
from mud.parser.handler import handleCmd
from client import isClient
import signals

clients = {}

def clientSentCmd( clientId, cmd ):
    isClient( clientId )
    assert isString( cmd )
    clients[ clientId ].cmds.append( cmd )


def clientFlushedCmdQueue( clientId ):
    isClient( clientId )
    del clients[ clientId ].cmds[:]


def pushCmdHandler( clientId, cmdHandler ):
    isClient( clientId )
    clients[ clientId ].cmdHandlers.append( cmdHandler )
    

def popCmdHandler( clientId ):
    isClient( clientId )
    if len( clients[ clientId ].cmdHandlers ) > 0:
        clients[ clientId ].cmdHandlers.pop()


def handleNextCmd( clientId ):
    isClient( clientId )
    handleNextCmdFromClientID( clientId )


def handleNextCmdForAllClients():
    for clientId in clients:
        handleNextCmdFromClientID( clientId )


##################
# Internal #######
##################

class Input:
    def __init__( self ):
        self.cmds = []
        self.cmdHandlers = []


def handleNextCmdFromClientID( clientId ):
    """ Internal use only """

    client = clients[ clientId ] 
    if len(client.cmds) == 0:
        return
    if len(client.cmdHandlers) == 0:
        return

    handleCmd( clientId, client.cmds.pop(0), client.cmdHandlers[-1])


def addClient( clientId ):
    """ Internal use only """
    clients[ clientId ] = Input()

signals.connect( addClient, signals.CONNECTED )


def removeClient( clientId ):
    """ Internal use only """
    del clients[ clientId ]

signals.connect( removeClient, signals.DISCONNECTED )


