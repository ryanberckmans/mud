from types import IntType
from mud import parser


clients = {}

def queueCmd( clientId, cmd ):
    assert type(clientId) == IntType, "client.queueCmd received clientId that wasn't an int"
    assert type(cmd) == StringType, "client.queueCmd received cmd that wasn't a string"
    assert clients[ clientId ], "client.queueCmd received a clientId that matches no clients (%s)" % clientId
    clients[ clientId ].cmds.append( cmd )


def disconnectClient( clientId ):
    #@todo
    pass


def newClient( clientId ):
    assert type(clientId) == IntType, "client.newClient received clientId that wasn't an int"
    assert clients[ clientId ] == None, "client.newClient received a duplicate clientId (%s)" % clientId
    clients[ clientId ] = Client( clientId )


def flushCmdQueue( clientId ):
    assert type(clientId) == IntType, "client.flushCmdQueue received clientId that wasn't an int"
    assert clients[ clientId ], "client.flushCmdQueue received a clientId that matches no clients (%s)" % clientId
    del clients[ clientId ].cmds[:]


def pushCmdHandler( clientId, cmdHandler ):
    assert type(clientId) == IntType, "client.pushCmdHandler received clientId that wasn't an int"
    assert clients[ clientId ], "client.pushCmdHandler received a clientId that matches no clients (%s)" % clientId
    clients[ clientId ].cmdHandlers.append( cmdHandler )
    

def popCmdHandler( clientId, cmdHandler):
    assert type(clientId) == IntType, "client.popCmdHandler received clientId that wasn't an int"
    assert clients[ clientId ], "client.popCmdHandler received a clientId that matches no clients (%s)" % clientId
    if len( clients[ clientId ].cmdHandlers ) > 0:
        clients[ clientId ].cmdHandlers.pop()


def handleNextCmd( clientId ):
    assert type(clientId) == IntType, "client.handleNextCmd received clientId that wasn't an int"
    assert clients[ clientId ], "client.handleNextCmd received a clientId that matches no clients (%s)" % clientId

    handleNextCmdFromClient( clients[ clientId ] )


def handleNextCmdForAllClients():
    for client in clients:
        handleNextCmdFromClient( client )


class Client:

    def __init__( self, ID ):
        assert type(ID) == IntType, "Client.init received ID that wasn't an int"

        self.ID = ID
        self.cmds = []
        self.cmdHandlers = []


##################
# Internal #######
##################

def handleNextCmdFromClient( client ):
    """ Internal use only """
    if len(client.cmds) == 0:
        return
    if len(client.cmdHandlers) == 0:
        return

    parser.handler.handleCmd( client, client.cmds.pop(0), client.cmdHandlers[-1])

        
