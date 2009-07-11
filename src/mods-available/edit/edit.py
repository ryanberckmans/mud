from util import endl
from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient
from mud.menu.textEditor import TextEditor


def submitEdit( clientId, text ):
    sendToClient( clientId, endl + "{!{FUYou edited:%s{@%s" % (endl, text) + endl )

def cmdEdit( clientId, remaining ):
    TextEditor( clientId, "TestTitle", "initial text\r\nromg!!!", submitEdit )
    pass

rootCmdMap.addCmd( "edit", cmdEdit )
