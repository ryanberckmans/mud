from types import StringType, FunctionType, BooleanType

import util
from exceptions import Match, NoMatch

# could call "parser" CmdContext
class CmdMap:

    def __init__(self):
        self.possibleNext = {}
        self.callback = None
        self.nextTokenNode = None
        self.allowAbbrev = True

    def addCmd(self, cmd, callback, allowAbbrev = True ):
        addCmdCheckPreconds( cmd, callback, allowAbbrev)
        addCmdFromNextToken( self, cmd, callback, allowAbbrev )
        return self


    def map( self, cmd):
        assert type(cmd) == StringType, "CmdMap.match received a cmd that wasn't a string"

        if len(cmd) == 0:
            raise NoMatch

        mapFromNextToken( self, cmd )
    

    # @todo add noAllowAbbrev and callback data to str
    #       without breaking unit tests
    def __str__helper(self, prefix=""):
        print "toString on CmdMap id %i with prefix %sEND. posnext (%s) nextTokenNode (%s)" % (id(self), prefix, str(self.possibleNext), not not self.nextTokenNode )
        toReturn = ""

        for char in self.possibleNext:
            toReturn += prefix + char + "\n"
        
        for char in self.possibleNext:
            if self.possibleNext[ char ].nextTokenNode:
                toReturn += self.possibleNext[ char ].nextTokenNode.__str__helper( "%s%s " % (prefix, char))
            
        for char in self.possibleNext:
            toReturn += self.possibleNext[char].__str__helper( "%s%s" % (prefix, char) )

        return toReturn


    def __str__(self):
        return self.__str__helper()





################################
###### Internal ###############
################################

def addCmdCheckPreconds( cmd, callback, allowAbbrev):
    assert type(cmd) == StringType, "CmdMap.addCmd received cmd that wasn't a string"
    assert len(cmd) > 0, "CmdMap.addCmd received cmd of length 0"
    assert type(callback) == FunctionType, "CmdMap.addCmd received callback that wasn't a function"
    assert type(allowAbbrev) == BooleanType, "CmdMap.addCmd received noAllowAbbrev that wasn't a bool"


def addCmdFromNextChar( cmdMap, char, cmdRemainingTokens, callback, allowAbbrev):

    print "next char: ", char
    if char not in cmdMap.possibleNext:
        cmdMap.possibleNext[ char ] = CmdMap()
        print "adding callback", callback
        cmdMap.possibleNext[ char ].callback = callback
        cmdMap.possibleNext[ char ].allowAbbrev = allowAbbrev
    else:
        if not cmdMap.possibleNext[ char ].allowAbbrev and allowAbbrev:
            cmdMap.possibleNext[ char ].callback = callback
            cmdMap.possibleNext[ char ].allowAbbrev = True

    if len(cmdRemainingTokens) > 0:
        print "should add next token node"
        if not cmdMap.possibleNext[ char ].nextTokenNode:
            print "adding next token node"
            cmdMap.possibleNext[ char ].nextTokenNode = CmdMap()

        cmdMap.possibleNext[ char ].nextTokenNode.addCmd( cmdRemainingTokens, callback, allowAbbrev )
        print "returned from nextTokenNode recurse"

    return cmdMap.possibleNext[ char ]
    

def addCmdFromNextToken( cmdMap, cmd, callback, allowAbbrev ):

    (cmdFirstToken, cmdRemainingTokens) = util.first_token(cmd)

    if len(cmdRemainingTokens) > 0:
        assert allowAbbrev, "CmdMap currently supports only monotoken no-allowAbbreviate commands"

    print "next token: %s      remaining: %s" % (cmdFirstToken, cmdRemainingTokens)

    assert len(cmdFirstToken) > 0, "CmdMap.addCmdFromNextToken received length 0 cmdFirstToken from util.firstToken. This should never happen... @Todo unless cmd is all whitespace"
        
    for char in cmdFirstToken:
        cmdMap = addCmdFromNextChar( cmdMap, char, cmdRemainingTokens, callback, allowAbbrev )

    if len(cmdRemainingTokens) == 0:
        cmdMap.allowAbbrev = True
            
 

def mapFromNextToken( cmdMap, cmd):

    (cmdFirstToken, cmdRemainingTokens) = util.first_token(cmd)
    print "next token: %s      remaining: %s" % (cmdFirstToken, cmdRemainingTokens)


    assert len(cmdFirstToken) > 0, "CmdMap.mapFromNextToken received length 0 cmdFirstToken from util.firstToken. This should never happen... @Todo unless cmd is all whitespace"

    for char in cmdFirstToken:
        print "next char %s" % char
        if char in cmdMap.possibleNext:
            cmdMap = cmdMap.possibleNext[ char ]
        else:
            raise NoMatch

    if len(cmdRemainingTokens) > 0 and cmdMap.nextTokenNode:
        try:
            cmdMap.nextTokenNode.map( cmdRemainingTokens )
        except NoMatch:
            pass
            #print "nextTokenNode.map raised NoMatch with remaining %s" % cmdRemainingTokens

    if not cmdMap.allowAbbrev:
        raise NoMatch

    assert cmdMap.callback, "CmdMap.map found a match with a null callback"

    if len(cmdRemainingTokens) == 0:
        cmdRemainingTokens = None

    raise Match(cmdMap.callback, cmdRemainingTokens)

    

def mapFromNextChar( cmdMap, cmd):
    pass
