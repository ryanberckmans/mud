from util import isList, isTuple, isString, isFunc, isBool, isDefined, endl
from mud.core.send import sendToClient
from mud.core.prompt import pushPrompt
from mud.core.cmds import pushCmdHandler
from mud.parser.cmdMap import CmdMap

def defaultInvalidSelectionCallback( clientId, menuStr ):
    sendToClient( clientId, menuStr )

class ValueSelector:

    def __init__( self, menuItems, selectionCallback, invalidSelectionCallback = None, alphabeticOptions = False ):
        """
        creates a menu widget, used to prompt the user to select a value from a set

        menuItems: [item] - the list of items to display in the menu.
                             item:  string - a line of text (e.g. header) to display in the menu
                                   or
                                   ( string, value ) - a description, value pair that the user can select

        selectionCallback: func - the function called with args ( clientId, selectedValue ) when the user selects a value

        invalidSelectionCallback: func - the function called with args ( clientId, clientInputRemaining )
                                         when the user's input doesn't map to a valid choice

        alphabeticOptions: bool - if true, use alphabetic, i.e. a..z, instead of numeric indices for the menu
        """
        assert isList( menuItems )
        assert isFunc( selectionCallback )
        if ( isDefined( invalidSelectionCallback ) ):
            assert isFunc( invalidSelectionCallback )
        else:
            invalidSelectionCallback = defaultInvalidSelectionCallback
        assert isBool( alphabeticOptions )
        
        assert len(menuItems) > 0

        self.prompt = ""
        self.menu   = ""
        self.cmdMap = CmdMap( invalidSelectionCallback )

        menuIndex = 1

        for item in menuItems:
            if isString( item ):
                self.menu += item + endl
                continue

            assert isTuple( item ) # item wasn't tuple or string
            assert len( item ) == 2

            ( itemDesc, itemValue ) = item
            
            assert isString( itemDesc )

            itemLabel = menuIndex
            if alphabeticOptions:
                itemLabel = chr(96 + menuIndex )

            self.menu += " {FC%s{FC) - {FU%s" % ( itemLabel, itemDesc ) + endl
            self.cmdMap.addCmd( "%s" % itemLabel, lambda clientId, remaining: selectionCallback( clientId, itemValue ) )
            menuIndex += 1

        self.menu += "{@"
            
    def activate( self, clientId ):
        """
        convenience function. pushes menu cmdMap and prompt, and displays menu
        """
        pushCmdHandler( clientId, self.cmdMap )
        pushPrompt( clientId, lambda x: self.prompt )
        sendToClient( clientId, self.menu )
        
                
            
                
