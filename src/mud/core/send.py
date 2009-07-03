from util import isString
from client import isClient, clients
import color

def sendToClient( clientId, msg ):
    isClient( clientId )
    sendToClientFromID( clientId, msg )

def sendToAll( msg ):
    for clientId in clients:
        sendToClientFromID( clientId, msg )


###############
## Internal ###
###############

def sendToClientFromID( clientId, msg ):
    """ Internal use only """
    assert isString( msg )
    msg = color.color( msg + "{@")
    if clientId in clientMsgs:
        clientMsgs[clientId] = clientMsgs[clientId] + msg
    else:
        clientMsgs[clientId] = msg



