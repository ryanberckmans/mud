from util import isList, isTuple, isString, isFunc, isBool, isDefined, endl
from mud.parser.cmdMap import CmdMap
from mud.core.send import sendToClient

def defaultInvalidSelectionCallback( clientId, menuStr ):
    sendToClient( clientId, menuStr )

class Form:

    def __init__( self, menuItems, submitCallback, invalidSelectionCallback = defaultInvalidSelectionCallback, alphabeticOptions = False ):
        """
        creates a form menu widget, used to contain other menu widgets
        """
        assert isList( menuItems )
        assert isFunc( submitCallback )
        if ( isDefined( invalidSelectionCallback ) ):
            assert isFunc( invalidSelectionCallback )
        assert isBool( alphabeticOptions )
        
        assert len(menuItems) > 0

        self.menuItems = menuItems
        self.prompt = ""
        self.cmdMap = CmdMap( invalidSelectionCallback )

        menuIndex = 1

        for item in self.menuItems:
            if isString( item ):
                continue

            assert isTuple( item ) # item wasn't tuple or string
            assert len( item ) == 3
            
            ( itemDesc, itemSelectedFunc, itemValueDescFunc ) = item
            
            assert isString( itemDesc )
            assert isFunc( itemSelectedFunc)
            assert isFunc( itemValueDescFunc)

            itemLabel = menuIndex
            if alphabeticOptions:
                itemLabel = chr(96 + menuIndex )

            self.cmdMap.addCmd( "%s" % itemLabel, lambda clientId, remaining: itemSelectedFunc( clientId ) )
            
            menuIndex += 1

    def menu( self, clientId ):
        menu = "{!"

        menuIndex = 1

        for item in menuItems:
            if isString( item ):
                menu += item + endl
                continue

            assert isTuple( item ) # item wasn't tuple or string
            assert len( item ) == 3
            
            ( itemDesc, itemSelectedFunc, itemValueDescFunc ) = item
            
            assert isString( itemDesc )
            assert isFunc( itemSelectedFunc)
            assert isFunc( itemValueDescFunc)

            itemLabel = menuIndex
            if alphabeticOptions:
                itemLabel = chr(96 + menuIndex )

            menu += " {FC%s{FG) {FU%s{FG: {FY" % ( itemLabel, itemDesc, itemValueDescFunc( clientId ) ) + endl

            menuIndex += 1


        return menu


        
        

            


        
        
