from types import *

import parser


class Client:

    def __init__( self, sendFunc ):
        assert type(sendFunc) == FunctionType, "Client.init received sendFunc that wasn't a function"
        
        self.cmds = []
        self.parsersStack = [[]]
        self.send = sendFunc
        
        self.defaultCmdCallback = lambda player, cmd: player.send("The command '%s' was not recognized.\n" % cmd )


    ### Prompt ###

    def prompt( self ):
        if len(self.prompts) == 0:
            return ""
        
        return self.prompts[-1]( self )


    def pushPrompt(self, promptFunc ):
        assert type(promptFunc) == FunctionType, "Client.pushPrompt received promptFunc that wasn't a function"
        self.prompts.append( promptFunc )


    def popPrompt(self, n = 1):
        assert type(n) == IntType, "Client.popPrompt received n that wasn't an int"
        assert n > 0, "Client.popPrompt received n that wasn't positive"

        try:
            while n > 0:
                self.prompts.pop()
                n -= 1
        except IndexError:
            pass


    ### Commands ###

    def addCmd( self, cmd ):
        assert type(cmd) == StringType, "Client.addCmd received cmd that wasn't a string"

        self.cmds.append( cmd )


    def flushCmds( self ):
        del self.cmds[:]


    def handleCmd( self ):

        if len(self.cmds) > 0:

            assert len( self.parsersStack ) > 0, "Client.handleCmd was going to handle a cmd with an empty parsers stack"
            parser.handle_cmd( self.cmds.pop(0), self, self.parsersStack[-1], self.defaultCmdCallback )



    ### Parsers ###

    def appendParser( self, parser ):

        assert parser, "Client.appendParser received null parser"
        assert len(self.parsersStack) > 0, "Client.appendParser detected empty parsersStack"

        self.parsersStack[-1].append( parser )


    def pushParsers( self, parsers ):
        assert type(parsers) == ListType, "Client.pushParsers received parsers that wasn't a list"

        self.parsersStack.append( parsers )


    def popParsers( self, n = 1):  # note parsersStack may never be empty
        assert type(n) == IntType, "Client.popParsers received n that wasn't an int"
        assert n > 0, "Client.popParsers received n that wasn't positive"

        try:
            while n > 0:
                self.parsersStack.pop()
                n -= 1
        except IndexError:
            self.parsersStack.append( [] ) # re-append the empty list of parsers

