from util import isList, isTuple, isString, isFunc, isBool, endl
from mud.parser.cmdMap import CmdMap

class ValueSelector:

    def __init__( self, menuItems, selectionCallback, invalidSelectionCallback = lambda x:x, alphabeticOptions = False ):
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
        assert isFunc( invalidSelectionCallback )
        assert isBool( alphabeticOptions )
        
        assert len(menuItems) > 0

        self.prompt = ""
        self.menu   = ""
        self.cmdMap = CmdMap( invalidSelectionCallback )

        for item in menuItems:
            if isString( item ):
                self.menu += item + endl
                continue

            assert isTuple( item ) # item wasn't tuple or string
            assert len( item ) == 2

            ( itemDesc, itemValue ) = item
            
            assert isString( itemDesc )
            

                
            
                
