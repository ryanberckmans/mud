


# for now, static prompts only
class Prompt:

    def __init__( self, 

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


