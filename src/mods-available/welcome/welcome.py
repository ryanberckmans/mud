import mud.core.mod as mod
import mud.core.signals as signals


def welcomeCallback( client ):
    client.send(
"""\r\n+--~--------------------~--+\r\n|Welcome to the framework! |\r\n|                          |\r\n|This message is provided  |\r\n|by mod-welcome =)         |\r\n+----~-----------~~--------+\r\n\r\n%s""" % mod.cmdList() )

mod.connect( welcomeCallback, signals.CONNECTED )
