import mud.core.mod as mod

def cmdChat( client, remaining ):
    client.send("You executed the cmd 'chat', remaining: %s\n" % remaining )

mod.addCmd( "chat", cmdChat )


