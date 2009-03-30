from util import isString
from mud.parser.cmdMap import CmdMap
from send import sendToClient
from cmds import pushCmdHandler, popCmdHandler
from rootCmdMap import rootCmdMap


class Mode:

    def __init__( self, modeName, modeCmd, modeDefaultCallback = None, modeAddDefaultCmds = True ):
        isString( modeCmd )
        isString( modeName )

        if not modeDefaultCallback:
            modeDefaultCallback = lambda clientId, remaining: sendToClient( clientId, "Invalid %s mode command. ({!{FC!{@ to exit, {!{FCcommands{@ for help)\r\n" % self.modeName )

        self.modeCmd = modeCmd
        self.modeName = modeName
        self.modeMap = CmdMap( modeDefaultCallback ) 

        def enterMode( clientId, remaining ):
            pushCmdHandler( clientId, self.modeMap )
            sendToClient( clientId, "\r\n{!{FG[{FYEntering %s mode{FG] {@({!{FC!{@ to exit)\r\n" % self.modeName)
            if modeAddDefaultCmds:
                sendToClient( clientId, self.modeMap.commands() )
            sendToClient( clientId, "\r\n" )

        def exitMode( clientId, remaining ):
            popCmdHandler( clientId )
            sendToClient( clientId, "{!{FG[{FYExiting %s Mode{FG]\r\n" % self.modeName)


        self.enterModeCallback = enterMode

        self.modeMap.addCmd("!", exitMode )
        if modeAddDefaultCmds:
            self.modeMap.addCmd("exit", exitMode )
            self.modeMap.addCmd("commands", lambda clientId, remaining: sendToClient( clientId, self.modeMap.commands() ) )


    def addCmd( self, cmd, callback, allowAbbrev=True ):
        self.modeMap.addCmd( cmd, callback, allowAbbrev )


    def register( self, parentMap=rootCmdMap):
        parentMap.addCmd( self.modeCmd, self.enterModeCallback )
            
