import mud.core.mod as mod
import mud.core.signals as signals


def welcomeCallback( client ):
    client.send(
"""
+--~--------------------~--+
|Welcome to the framework! |
|                          |
|This welcome message      |
|is provided by mod-welcome|
|and may be disabled by    |
|destroying the symlink =) |
+----~-----------~~--------+

""" )

mod.connect( welcomeCallback, signals.CONNECTED )
