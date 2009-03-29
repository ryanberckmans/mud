import mud.core.mod as mod
from mud.core.cmds import pushCmdHandler, popCmdHandler
from mud.core.send import sendToClient, sendToAll
from mud.parser.cmdMap import CmdMap


def cmdChat( clientId, remaining ):
    if not remaining or len(remaining) == 0:
        sendToClient( clientId, "Usage: chat msg\r\n")
        return
    
    sendToAll("{!{FC%i chats to everybody, '%s'\r\n" % ( clientId, remaining ) )

mod.addCmd( "chat", cmdChat )


chatModeMap = CmdMap( cmdChat )


def cmdExitChatMode( clientId, remaining ):
    popCmdHandler( clientId )
    sendToClient( clientId, "{!{FG[{FYExiting Chat Mode{FG]\r\n")


chatModeMap.addCmd("!", cmdExitChatMode )

def cmdEnterChatMode( clientId, remaining ):
    pushCmdHandler( clientId, chatModeMap )
    sendToClient( clientId, "\r\n{!{FG[{FYEntering Chat Mode{FG] {@({!{FC!{@ to exit)\r\n")

mod.addCmd( "mode chat", cmdEnterChatMode )
