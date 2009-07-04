from util import isList, isTuple, isString, isFunc, isBool, isDefined, endl
from mud.parser.cmdMap import CmdMap
from mud.core.send import sendToClient
from mud.core.cmds import pushCmdHandler
from mud.core.prompt import pushPrompt

def defaultInvalidSelectionCallback( clientId, menuFunc ):
    sendToClient( clientId, menuFunc( clientId ) )

class Form:

    def __init__( self, menuItems, submitCallback, invalidSelectionCallback = "DEFAULT", alphabeticOptions = False ):
        """
        creates a form menu widget, used to contain other menu widgets
        """
        assert isList( menuItems )
        assert isFunc( submitCallback )
        assert isBool( alphabeticOptions )


        # invalidSelectionCallback may be:
        #  "DEFAULT" - an internal hack to bind to self.menu
        #  None      - meaning an invalid selection defers to a later cmdHandler
        #  Func      - a client-supplied invalidSelectionCallback
        if invalidSelectionCallback == "DEFAULT":
           invalidSelectionCallback = lambda clientId, remaining: defaultInvalidSelectionCallback( clientId, self.menu)
        if isDefined( invalidSelectionCallback ):
            assert isFunc( invalidSelectionCallback )
        
        
        assert len(menuItems) > 0

        self.menuItems = menuItems
        self.prompt = ""
        self.cmdMap = CmdMap( invalidSelectionCallback )
        self.alphabeticOptions = alphabeticOptions

        menuIndex = 1

        self.cmdMap.addCmd( "f", lambda clientId, remaining: submitCallback( clientId ) )
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
            if self.alphabeticOptions:
                itemLabel = chr(96 + menuIndex )

            self.cmdMap.addCmd( "%s" % itemLabel, lambda clientId, remaining: itemSelectedFunc( clientId ) )
            
            menuIndex += 1

    def menu( self, clientId ):
        menu = "{!"

        menuIndex = 1

        for item in self.menuItems:
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
            if self.alphabeticOptions:
                itemLabel = chr(96 + menuIndex )

            menu += " {FC%s{FG) {FU%s{FG: {FY%s" % ( itemLabel, itemDesc, itemValueDescFunc( clientId ) ) + endl

            menuIndex += 1

        menu += " {FCf{FG) finish " + endl

        return menu

    def activate( self, clientId ):
        """
        convenience function. pushes menu cmdMap and prompt, and displays menu
        """
        pushCmdHandler( clientId, self.cmdMap )
        pushPrompt( clientId, lambda x: self.prompt )
        sendToClient( clientId, self.menu( clientId ) )
        

        
        

            


        
        
