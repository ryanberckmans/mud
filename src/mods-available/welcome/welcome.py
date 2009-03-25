import mud.core.mod as mod
import mud.core.signals as signals


def welcomeCallback( client ):
    client.send(
"""\r\n
+--~--------------------~--+\r\n
|Welcome to the framework! |\r\n
|                          |
|This message is provided  |
|by mod-welcome =)         |
+----~-----------~~--------+
""" )

mod.connect( welcomeCallback, signals.CONNECTED )
