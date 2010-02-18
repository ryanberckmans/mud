from util import endl
from mud.core.rootCmdMap import rootCmdMap
from mud.menu.form import Form
from mud.core.cmds import popCmdHandler
from mud.core.prompt import popPrompt
from mud.core.send import sendToClient
import colorSelector


def submenuSelectionCallback( clientId ):
    sendToClient( clientId, menu( clientId ))

colorMenu = colorSelector.ColorSelector( submenuSelectionCallback )

def colorValueDescFunc( clientId ):
    if clientId in colorMenu.colors:
        return colorMenu.colors[ clientId ] + "is this color"
    return "<select a color>"

menuItems = [
    endl + "{FYChat Configuration:",
    ( "font color", colorMenu.menu.activate, colorValueDescFunc ),
    ]


def finishCallback( clientId, abort = False ):
    popCmdHandler( clientId )
    popPrompt( clientId )

form = Form( menuItems, finishCallback )
menu = form.menu

rootCmdMap.addCmd( "config chat", lambda clientId, remaining: form.activate( clientId ) )
