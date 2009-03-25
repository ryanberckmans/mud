from pydispatch import dispatcher
import signals
import mud.parser.cmdMap as cmdMap

def connect( callback, signal ):
    dispatcher.connect( callback, signal )

def addCmd( cmd, callback, allowAbbrev=True ):
    rootCmdsMap.addCmd( cmd, callback, allowAbbrev )
    rootCmdsList.append( cmd )

###############
# INTERNAL ####
###############

rootCmdsMap = cmdMap.CmdMap()
rootCmdsList = []


def addRootMap( client ):
    client.cmdHandlers.append( rootCmdsMap )

def cmdList():
    cmdsStr = "Commands:\r\n"
    for cmd in rootCmdsList:
        cmdsStr = cmdsStr + "%s\r\n" % cmd

    return cmdsStr

connect( addRootMap, signals.CONNECTED )





    


