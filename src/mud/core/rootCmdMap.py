from pydispatch import dispatcher
from mud.parser.cmdMap import CmdMap
from cmds import pushCmdHandler
from send import sendToClient
import signals

def invalidCmd( clientId, remaining ):
    sendToClient( clientId, "Invalid command. ({!{FCcommands{@ for help)\r\n")

rootCmdMap = CmdMap( invalidCmd )
rootCmdMap.addCmd("commands", lambda clientId, remaining: sendToClient( clientId, rootCmdMap.commands() ) )

def addRootMap( clientId ):
    pushCmdHandler( clientId, rootCmdMap )

signals.connect( addRootMap, signals.CONNECTED )


