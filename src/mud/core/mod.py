from pydispatch import dispatcher
import mud.parser.cmdMap as cmdMap
from cmds import pushCmdHandler
from send import sendToClient
import signals

def addCmd( cmd, callback, allowAbbrev=True ):
    rootCmdsMap.addCmd( cmd, callback, allowAbbrev )

###############
# INTERNAL ####
###############

def invalidCmd( clientId, remaining ):
    sendToClient( clientId, "Invalid command. ({!{FCcommands{@ for help)\r\n")

rootCmdsMap = cmdMap.CmdMap( invalidCmd )

def addRootMap( clientId ):
    pushCmdHandler( clientId, rootCmdsMap )

def commands():
    return rootCmdsMap.commands()

signals.connect( addRootMap, signals.CONNECTED )


