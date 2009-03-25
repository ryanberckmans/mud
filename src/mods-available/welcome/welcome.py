import mud.core.mod as mod
import mud.core.signals as signals


def welcomeCallback( client ):
    client.send(
"""
+--~--------------------~--+
|Welcome to the framework! |
|                          |
|This message is provided  |
|by mod-welcome =)         |
+----~-----------~~--------+

""" )

mod.connect( welcomeCallback, signals.CONNECTED )
