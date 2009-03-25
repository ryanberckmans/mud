import mud.core.mod as mod
import mud.core.signals as signals


welcomeMessage = """{@{!{FG     ________             ________ \r\n{FG    / ____  /\           /\  ____ \ \r\n{FG   / /\__/ / _\_________/_ \ \__/\ \ \r\n{FG  / /_/_/ / /             \ \ \_\_\ \ \r\n{FG /_______/ /_______________\ \_______\ \r\n{FG \  ____ \ \               / / ____  / \r\n{FG  \ \ \_\ \ \_____________/ / /_/ / / \r\n{FG   \ \/__\ \  /{FR N O T A{FG \  / /__\/ / \r\n{FG    \_______\/{FY M   U   D{FG \/_______/ \r\n{FG  \r\n       {BR{FW+{BB {FRC a t a l y s t i c a {BR{FW+{@ \r\n \r\n%s"""


def welcomeCallback( client ):
    client.send( welcomeMessage % mod.commands() )
    
mod.connect( welcomeCallback, signals.CONNECTED )
