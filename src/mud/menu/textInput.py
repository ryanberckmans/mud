from util import isFunc, isInt, isString
from mud.parser.cmdMap import CmdMap
from mud.core.send import sendToClient
from mud.core.cmds import pushCmdHandler, popCmdHandler

prompt = "{!{FU<text input> "

def _submitText( clientId, submitCallback, text ):
    assert isFunc( submitCallback)
    assert isString( text )
    
    popCmdHandler( clientId )

    submitCallback( clientId, text )

def getOneLine( clientId, submitCallback ):
    """
    activates a text input widget for clientId, which returns one line of text

    submitCallback: func( clientId, text )
    """
    
    assert isInt( clientId )
    assert isFunc( submitCallback)

    pushCmdHandler( clientId, CmdMap( lambda x, remaining: _submitText( x, submitCallback, remaining ) ) )
