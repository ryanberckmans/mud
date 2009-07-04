from util import endl
import mud.menu.valueSelector as valueSelector
from mud.core.cmds import popCmdHandler
from mud.core.prompt import popPrompt

class ColorSelector:
    def __init__( self, selectionCallback ):
        self.colors = {}

        menuItems = [
            endl + "Select a font color:",
            ( "{FCcyan", "{FC" ),
            ( "{FYyellow", "{FY" ),
            ( "{FRred", "{FR" ),
            ]

        def colorSelected( clientId, color ):
            self.colors[ clientId ] = color
            popCmdHandler( clientId )
            popPrompt( clientId )
            selectionCallback( clientId )

        self.menu = valueSelector.ValueSelector( menuItems, colorSelected, "DEFAULT", True )
        self.menu.prompt = endl + "{!{FBselect a color >"


