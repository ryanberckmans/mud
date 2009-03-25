from pydispatch import dispatcher
import signals
import mud.parser.cmdMap as cmdMap

def connect( callback, signal ):
    dispatcher.connect( callback, signal )

def addCmd( cmd, callback, allowAbbrev=True ):
    regularCmdsMap.addCmd( cmd, callback, allowAbbrev )



###############
# INTERNAL ####
###############

regularCmdsMap = cmdMap.CmdMap()
def addRegularMap( client ):
    client.cmdHandlers.append( regularCmdsMap )

connect( addRegularMap, signals.CONNECTED )


    


