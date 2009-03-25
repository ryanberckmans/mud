import mud.core.mod as mod
import mud.core.client as clientModule
import mud.parser.cmdMap as cmdMap

def cmdChat( client, remaining ):
    if not remaining or len(remaining) == 0:
        client.send("Usage: chat msg\r\n")
        return
    
    clientModule.sendToAll("{!{FC%i chats to everybody, '%s'\r\n" % ( client.ID, remaining ) )

mod.addCmd( "chat", cmdChat )


chatModeMap = cmdMap.CmdMap( cmdChat )


def cmdExitChatMode( client, remaining ):
    client.cmdHandlers.pop()
    client.send("{!{FG[{FYExiting Chat Mode{FG]\r\n")


chatModeMap.addCmd("!", cmdExitChatMode )

def cmdEnterChatMode( client, remaining ):
    client.cmdHandlers.append( chatModeMap )
    client.send("{!{FG[{FYEntering Chat Mode{FG] {@({!{FC!{@ to exit)\r\n")

mod.addCmd( "mode chat", cmdEnterChatMode )
