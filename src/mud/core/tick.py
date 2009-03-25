from pydispatch import dispatcher
from cppTypes import *
import loadMods
import client
import signals

newClients = IntVector()
disconnectedClients = IntVector()
flushedClients = IntVector()
clientCmds = IntStringMap()
clientMsgs = IntStringMap()

## HACK
## client needs clientMsgs to send ?? 
def send( clientId, msg):
    if clientId in clientMsgs:
        clientMsgs[clientId] = clientMsgs[clientId] + msg
    else:
        clientMsgs[clientId] = msg

client.send = send
## END HACK

def tick():

    dispatcher.send( signals.BEFORE_TICK, tick )

    for clientId in disconnectedClients:
        client.disconnectClient( clientId )

    for clientId in newClients:
        client.newClient( clientId )

    for clientId in flushedClients:
        client.flushCmdQueue( clientId )

    for cmd in clientCmds:
        client.queueCmd( cmd.key(), cmd.data() )

    client.handleNextCmdForAllClients()

    dispatcher.send( signals.AFTER_TICK, tick )

