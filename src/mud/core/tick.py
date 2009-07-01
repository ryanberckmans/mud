from pydispatch import dispatcher
from cppTypes import *
import send # HACK HACK
import loadMods
import cmds
import prompt
import client
import signals

newClients = IntVector()
disconnectedClients = IntVector()
flushedClients = IntVector()
clientCmds = IntStringMap()
clientMsgs = IntStringMap()
## HACK
send.clientMsgs = clientMsgs
## END HACK

def tick():

    dispatcher.send( signals.BEFORE_TICK, tick )

    for clientId in disconnectedClients:
        client.clientDisconnectedFromServer( clientId )

    for clientId in newClients:
        client.clientConnectedToServer( clientId )

    for clientId in flushedClients:
        cmds.clientFlushedCmdQueue( clientId )

    for cmd in clientCmds:
        cmds.clientSentCmd( cmd.key(), cmd.data() )

    cmds.handleNextCmdForAllClients()

    def keys( intStringMap ):
        return map( lambda i: i.key(), intStringMap )

    map( lambda clientId: send.sendToClient( clientId, prompt.prompt( clientId, clientId ) )  ,  list(set( keys( clientCmds ) ).union( keys( send.clientMsgs ) ) ) )

    dispatcher.send( signals.AFTER_TICK, tick )

