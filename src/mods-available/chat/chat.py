import mud.core.mod as mod
import mud.core.client as client

def cmdChat( chatter, remaining ):
    if not remaining or len(remaining) == 0:
        chatter.send("Usage: chat msg\r\n")
        return
    
    client.sendToAll( "%i chats to everybody, '%s'\r\n" % ( chatter.ID, remaining ) )

mod.addCmd( "chat", cmdChat )


