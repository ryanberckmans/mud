import mud.core.mod as mod


def cmdCommands( client, remaining ):
    client.send( mod.cmdList() )

mod.addCmd( "commands", cmdCommands )

