from util import isFunc, isInt, isDefined
from clientTracker import ClientTracker

def prompt( clientId, obj ):
    assert tracker.isClient( clientId )

    return tracker.clients[ clientId ].prompt( obj )

def pushPrompt( clientId, promptFunc ):
    assert tracker.isClient( clientId )

    tracker.clients[ clientId ].pushPrompt( promptFunc )

def popPrompt( clientId, n ):
    assert tracker.isClient( clientId )

    if ( isDefined( n ) ):
        tracker.clients[ clientId ].popPrompt( n )
    else:
        tracker.clients[ clientId ].popPrompt()

    
##################
# Internal #######
##################

class _Prompt:

    def __init__( self, clientId ):
        isInt( clientId )
        
        self.prompts = []
        self.clientId = clientId  # currently unused, satisfies ClientTracker signature

        # temp default, should really broadcast PROMPT_CREATED
        self.pushPrompt( lambda clientId: "\n{!{FB<client {FG%s{FB> " % clientId )

    def prompt( self, obj ): # where obj enables promptFunc to retrieve state, e.g. obj may be a Mob
        if len(self.prompts) == 0:
            return ""
        
        return self.prompts[-1]( obj )


    def pushPrompt(self, promptFunc ):
        assert isFunc( promptFunc )

        self.prompts.append( promptFunc )


    def popPrompt(self, n = 1):
        assert isInt( n )
        assert n > 0

        try:
            while n > 0:
                self.prompts.pop()
                n -= 1
        except IndexError:
            pass

tracker = ClientTracker( _Prompt )
