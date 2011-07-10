from util import isFunc, isString, isDefined, endl
from mud.core.send import sendToClient
from mud.core.prompt import pushPrompt, popPrompt
from mud.core.cmds import pushCmdHandler, popCmdHandler
from mud.parser.cmdMap import CmdMap

class TextEditor:

    def __init__( self, clientId, nameOfEdit, initialText, submitCallback, invalidSelectionCallback = "DEFAULT" ):
        """
        creates a text editor widget and activates it for clientId, used to input arbitrarily formatted text

        submitCallback: func( clientId, text )
        """

        assert isString( nameOfEdit )
        assert isString( initialText )
        assert isFunc( submitCallback )

        # invalidSelectionCallback may be:
        #  "DEFAULT" - an internal hack to bind to self.menu
        #  None      - meaning an invalid selection defers to a later cmdHandler
        #  Func      - a client-supplied invalidSelectionCallback
        if invalidSelectionCallback == "DEFAULT":
           invalidSelectionCallback = lambda clientId, remaining: _defaultInvalidSelectionCallback( clientId, self.menu)
        if isDefined( invalidSelectionCallback ):
            assert isFunc( invalidSelectionCallback )

        self.text = initialText
        self.submitCallback = submitCallback
        self.menu = endl + "{!{FYEditing %s" % nameOfEdit + endl
        self.cmdMap = CmdMap( invalidSelectionCallback )

        _addDisplay( self )
        _addFinish( self )

        self.menu += endl

        _activate( clientId, self )

_prompt = "{!{FU<text editor>"
        
def _addDisplay( editor ):
    editor.menu += " {FCt{FG) {FUdisplay text" + endl
    editor.cmdMap.addCmd( "t", lambda clientId, remaining: _displayText( clientId, editor )  )

def _addFinish( editor ):
    editor.menu += " {FCf{FG) finish " + endl
    editor.cmdMap.addCmd( "f", lambda clientId, remaining: _finish( clientId, editor ) )
                            
def _defaultInvalidSelectionCallback( clientId, menu ):
    sendToClient( clientId, menu )

def _activate( clientId, textEditor ):
    pushCmdHandler( clientId, textEditor.cmdMap )
    pushPrompt( clientId, lambda clientId: _prompt )
    sendToClient( clientId, textEditor.menu )

def _finish( clientId, textEditor ):
    popCmdHandler( clientId )
    popPrompt( clientId )
    textEditor.submitCallback( clientId, textEditor.text )

def _displayText( clientId, textEditor ):
    sendToClient( clientId, textEditor.text + endl + textEditor.menu )


class _Buffer:

    def __init__( self, initialText=None):

        self.lines = []
        
        if initialText:
            _stringToLines( initialText )

    def wipe( self ):
        self.lines = []

    def appendLine( self, string ):
        pass

    def _stringToLines( self, initialText):
        pass
