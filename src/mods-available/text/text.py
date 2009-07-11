from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient
from mud.core.prompt import pushPrompt, popPrompt
from mud.menu.textInput import getOneLine, prompt as textPrompt


def textCallback( clientId, text ):
    sendToClient( clientId, "{!{FUYou typed:{FG %s" % text )
    popPrompt( clientId )

def cmdText( clientId, remaining ):
    getOneLine( clientId, textCallback )
    pushPrompt( clientId, lambda x: textPrompt )

rootCmdMap.addCmd( "text", cmdText )
    
    
