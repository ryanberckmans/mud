from cppTypes import *
import client

newClients = IntVector()
disconnectedClients = IntVector()
flushedClients = IntVector()
clientCmds = IntStringMap()
clientMsgs = IntStringMap()

## HACK
## client needs clientMsgs to send ?? 
def send( clientId, msg):
    if clientId in clientMsgs:
        msgs[clientId] = clientMsgs[clientId] + msg
    else:
        msgs[clientId] = msg

client.send = send
## END HACK

def tick():

    for clientId in disconnectedClients:
        client.disconnectClient( clientId )

    for clientId in newClients:
        client.newClient( clientId )

    for clientId in flushedClients:
        client.flushCmdQueue( clientId )

    for cmd in clientCmds:
        client.queueCmd( cmd.key(), cmd.data() )

    client.handleNextCmdForAllClients()



