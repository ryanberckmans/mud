from pydispatch import dispatcher
import signals
import mud.parser.cmdMap as cmdMap

def connect( callback, signal ):
    dispatcher.connect( callback, signal )

def addCmd( cmd, callback, allowAbbrev=True ):
    rootCmdsMap.addCmd( cmd, callback, allowAbbrev )

###############
# INTERNAL ####
###############

def invalidCmd( client, remaining ):
    client.send("Invalid command. ({!{FCcommands{@ for help)\r\n")

rootCmdsMap = cmdMap.CmdMap( invalidCmd )

def addRootMap( client ):
    client.cmdHandlers.append( rootCmdsMap )

def commands():
    return rootCmdsMap.commands()


connect( addRootMap, signals.CONNECTED )





    


