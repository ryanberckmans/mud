from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient, sendToAll
from mud.core.mode import Mode


def cmdChat( clientId, remaining ):
    if not remaining or len(remaining) == 0:
        sendToClient( clientId, "Usage: chat msg\r\n")
        return

    cmdChatFromMsg( clientId, remaining )
    

def cmdChatFromMsg( clientId, msg):
    sendToAll("{!{FC%i chats to everybody, '%s'\r\n" % ( clientId, msg ) )


rootCmdMap.addCmd( "chat", cmdChat )

chatMode = Mode("chat", "mode chat", cmdChatFromMsg, False )
chatMode.register()

