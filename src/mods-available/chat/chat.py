import mud.core.mod as mod

def cmdChat( client, remaining ):
    client.send("You executed chat!")

mod.addCmd( "chat", cmdChat )


