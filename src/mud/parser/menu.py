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

    def __init__( self, menuPairs, finishedCallback, menuHeader = None, menuFooter = None, invalidSelectionCallback = None ):
        """
         menuPairs: [ ( menuItemDescription: str, menuItemValue: any type ) ]
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

        for (menuItemDescription, menuItemValue) in menuPairs:
            isStr( menuItemDescription)
            self.menuStr = self.menuStr + "{FC%i{FG) - {FU%s\r\n" % ( menuIndex, menuItemDescription )
            self.menuMap.addCmd( "%i" % menuIndex, finishMenuWithValue( menuItemValue ) )
            menuIndex += 1

        self.menuStr += "{@"
            
        if menuHeader:
            isStr( menuHeader )
            self.menuStr = menuHeader + self.menuStr

        if menuFooter:
            isStr( menuFooter )
            self.menuStr = self.menuStr + menuFooter


    def use( self, clientId ):
        sendToClient( clientId, self.menuStr )
        pushCmdHandler( clientId, self.menuMap )

        

