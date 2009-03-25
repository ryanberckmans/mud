from cppTypes import *
import client

newClients = IntVector()
disconnectedClients = IntVector()
flushedClients = IntVector()
clientCmds = IntStringMap()
clientMsgs = IntStringMap()

def tick():

    for clientId in disconnectedClients:
        client.disconnectClient( clientId )

    for clientId in newClients:
        client.newClient( clientId )

    for clientId in flushedClients:
        client.flushClient( clientId )

    for cmd in clientCmds:
        client.queueCmd( cmd.key(), cmd.data() )

    client.handleNextCmdForAllClients()



