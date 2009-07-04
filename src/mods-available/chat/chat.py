from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient, sendToAll
from mud.core.mode import Mode
from chatconfig import colorMenu


def cmdChat( clientId, remaining ):
    if not remaining or len(remaining) == 0:
        sendToClient( clientId, "Usage: chat msg\r\n")
        return

    cmdChatFromMsg( clientId, remaining )
    

def cmdChatFromMsg( clientId, msg):
    color = "{FC"
    if clientId in colorMenu.colors:
        color = colorMenu.colors[ clientId ]

    sendToAll("{!{FC%i chats to everybody, '%s%s{FC'\r\n" % ( clientId, color, msg ) )


rootCmdMap.addCmd( "chat", cmdChat )

chatMode = Mode("chat", "mode chat", cmdChatFromMsg, False )
chatMode.register()

