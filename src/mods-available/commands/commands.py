import mud.core.mod as mod
from mud.core.send import sendToClient

def cmdCommands( clientId, remaining ):
    sendToClient( clientId, mod.commands() )

mod.addCmd( "commands", cmdCommands )

