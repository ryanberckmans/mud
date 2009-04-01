from util import isList, isStr, isFunc
from mud.core.send import sendToClient
from mud.core.cmds import popCmdHandler, pushCmdHandler
from cmdMap import CmdMap



def defaultInvalidSelectionCallback( clientId, menuStr ):
    sendToClient( clientId, menuStr )

def finishMenu( clientId, finishedCallback, value):
    popCmdHandler( clientId )
    finishedCallback( clientId, value )

class Menu:

    def __init__( self, menuPairs, finishedCallback, invalidSelectionCallback = None ):
        """
         menuPairs: [], each element is string or (string, any type)
         finishedCallback: f( clientId, selectedValue )
         invalidSelectionCallback: f( clientId, remaining )
         """
        isList( menuPairs)
        isFunc( finishedCallback)

        if invalidSelectionCallback:
            isFunc( invalidSelectionCallback )
        else:
            invalidSelectionCallback = lambda clientId, remaining: defaultInvalidSelectionCallback( clientId, self.menuStr )

        self.menuStr = "{!"
        self.menuMap = CmdMap( invalidSelectionCallback )
        menuIndex = 1

        def finishMenuWithValue( value ):
            return lambda clientId, remaining: finishMenu( clientId, finishedCallback, value )

        for item in menuPairs:
            if type(item) == str:
                self.menuStr += item + "\r\n"
                continue

            ( menuItemDescription, menuItemValue ) = item
                
            isStr( menuItemDescription)
            self.menuStr = self.menuStr + " {FC%i{FG) - {FU%s\r\n" % ( menuIndex, menuItemDescription )
            self.menuMap.addCmd( "%i" % menuIndex, finishMenuWithValue( menuItemValue ) )
            menuIndex += 1

        self.menuStr += "{@"
            

    def use( self, clientId ):
        sendToClient( clientId, self.menuStr )
        pushCmdHandler( clientId, self.menuMap )

        

