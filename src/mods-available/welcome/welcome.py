from mud.core.rootCmdMap import rootCmdMap
import mud.core.signals as signals
from mud.core.send import sendToClient


welcomeMessage = """{@{!{FG     ________             ________ \r\n{FG    / ____  /\           /\  ____ \ \r\n{FG   / /\__/ / _\_________/_ \ \__/\ \ \r\n{FG  / /_/_/ / /             \ \ \_\_\ \ \r\n{FG /_______/ /_______________\ \_______\ \r\n{FG \  ____ \ \               / / ____  / \r\n{FG  \ \ \_\ \ \_____________/ / /_/ / / \r\n{FG   \ \/__\ \  /{FR N O T A{FG \  / /__\/ / \r\n{FG    \_______\/{FY M   U   D{FG \/_______/ \r\n{FG  \r\n       {BR{FW+{BB {FRC a t a l y s t i c a {BR{FW+{@{BB \r\n \r\n%s"""


def welcomeCallback( clientId ):
    sendToClient( clientId, welcomeMessage % rootCmdMap.commands() )
    
signals.connect( welcomeCallback, signals.CONNECTED )
