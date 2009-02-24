from types import *
import parser


def temporary_invalid_cmd( player, remaining):
    print "Invalid command :)"

class Mob:

    def __init__( self, ID):
        self.ID = ID
        self.prompts = []
        self.cmds = []
        self.parsers_stack = [[]]



    ### Prompt ###

    def prompt( self ):
        if len(self.prompts) == 0:
            return ""
        
        return self.prompts[-1]( self )


    def push_prompt(self, prompt_func ):
        assert type(prompt_func) == FunctionType, "Mob.push_prompt received prompt_func that wasn't a function"
        self.prompts.append( prompt_func )


    def pop_prompt(self, n = 1):
        assert type(n) == IntType, "Mob.pop_prompt received n that wasn't an int"
        assert n > 0, "Mob.pop_prompt received n that wasn't positive"

        try:
            while n > 0:
                self.prompts.pop()
                n -= 1
        except IndexError:
            pass



    ### Commands ###

    def add_cmd( self, cmd ):
        assert type(cmd) == StringType, "Mob.add_cmd received cmd that wasn't a string"

        self.cmds.append( cmd )


    def flush_cmds( self ):
        del self.cmds[:]


    def handle_cmd( self ):

        if len(self.cmds) > 0:

            assert len( self.parsers_stack ) > 0, "Mob.handle_cmd was going to handle a cmd with an empty parsers stack"

            parser.handle_cmd( self.cmds.pop(0), self, self.parsers_stack[-1], temporary_invalid_cmd )



    ### Parsers ###

    def append_parser( self, parser ):

        assert parser, "Mob.append_parser received null parser"
        assert len(self.parsers_stack) > 0, "Mob.append_parser detected empty parsers_stack"

        self.parsers_stack[-1].append( parser )


    def push_parsers( self, parsers ):
        assert type(parsers) == ListType, "Mob.push_parsers received parsers that wasn't a list"

        self.parsers_stack.append( parsers )


    def pop_parsers( self, n = 1):  # note parsers_stack may never be empty
        assert type(n) == IntType, "Mob.pop_parsers received n that wasn't an int"
        assert n > 0, "Mob.pop_parsers received n that wasn't positive"

        try:
            while n > 0:
                self.parsers_stack.pop()
                n -= 1
        except IndexError:
            self.parsers_stack.append( [] ) # re-append the empty list of parsers


        
        


        



    

    

        
    
