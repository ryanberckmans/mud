import mud.core.mod as mod


def cmdCommands( client, remaining ):
    client.send( mod.commands() )

mod.addCmd( "commands", cmdCommands )

