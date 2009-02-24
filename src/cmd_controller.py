import parser
from types import StringType

class CmdController:

    def __init__( self ):
        self.cmds = []
        self.parsersStack = [[]]
        self.defaultCmdCallback = None
        
    
    ### Commands ###

    def add_cmd( self, cmd ):
        assert type(cmd) == StringType, "LogonSequence.add_cmd received cmd that wasn't a string"

        self.cmds.append( cmd )


    def flush_cmds( self ):
        del self.cmds[:]


    def handle_cmd( self ):

        if len(self.cmds) > 0:

            assert len( self.parsersStack ) > 0, "LogonSequence.handle_cmd was going to handle a cmd with an empty parsers stack"

            parser.handle_cmd( self.cmds.pop(0), self, self.parsersStack[-1], self.defaultCmdCallback )


   ### Parsers ###

    def append_parser( self, parser ):

        assert parser, "LogonSequence.append_parser received null parser"
        assert len(self.parsersStack) > 0, "LogonSequence.append_parser detected empty parsersStack"

        self.parsersStack[-1].append( parser )


    def push_parsers( self, parsers ):
        assert type(parsers) == ListType, "LogonSequence.push_parsers received parsers that wasn't a list"

        self.parsersStack.append( parsers )


    def pop_parsers( self, n = 1):  # note parsersStack may never be empty
        assert type(n) == IntType, "LogonSequence.pop_parsers received n that wasn't an int"
        assert n > 0, "LogonSequence.pop_parsers received n that wasn't positive"

        try:
            while n > 0:
                self.parsersStack.pop()
                n -= 1
        except IndexError:
            self.parsersStack.append( [] ) # re-append the empty list of parsers
