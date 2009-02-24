from types import *
import util


# TrieNode exceptions

class Match(Exception):
    def __init__(self, callback, remaining=None):

        assert callback, "Match constructor received null callback"

        self.callback = callback
        self.remaining = remaining

    def __str__(self):
        # @todo add callback desc
        return "Match (remaining input: " + self.remaining + ")"

class NoMatch(Exception):

    def __str__(self):
        return "NoMatch"

class TrieNode:

    def __init__(self):
        self.possible_next = {}
        self.callback = None
        self.next_token_node = None
        self.no_abbrev = False

    # string cmd
    # callback is the function corresponding to the match
    # no_abbrev==true specifies no partial matches permitted
    def add( self, cmd, callback, no_abbrev = False ):

        assert type(cmd) == StringType, "TrieNode.add received cmd that wasn't a string"
        assert type(callback) == FunctionType, "TrieNode.add received callback that wasn't a function"
        assert type(no_abbrev) == BooleanType, "TrieNode.add received no_abbrev that wasn't a bool"

        (first, cmd) = util.first_token( cmd )

        assert len(first) > 0, "TrieNode.add received first from util.first_token with length 0"

        node = self

        for next_char in first:
             #print "next char: ", next_char

             if next_char not in node.possible_next:
                 node.possible_next[ next_char ] = TrieNode()
                 #print "adding callback", callback
                 node.possible_next[ next_char ].callback = callback
                 node.possible_next[ next_char ].no_abbrev = no_abbrev
             else:
                 if node.possible_next[ next_char ].no_abbrev and not no_abbrev:
                     node.possible_next[ next_char ].callback = callback
                     node.possible_next[ next_char ].no_abbrev = False

             if len(cmd) > 0:
                 #print "should add next token node"
                 if not node.possible_next[ next_char ].next_token_node:
                     node.possible_next[ next_char ].next_token_node = TrieNode()

                 node.possible_next[ next_char ].next_token_node.add( cmd, callback, no_abbrev )

             node = node.possible_next[ next_char ]



        if len(cmd) == 0:
            node.no_abbrev = False

        return self

    # str is cmd to be matched
    def match( self, cmd ):

         #print " match started!"

         assert type(cmd) == StringType, "TrieNode.match received a cmd that wasn't a string"

         if len(cmd) == 0:
             raise NoMatch
    
         (first, cmd) = util.first_token(cmd)

         #print " match with first=", first
         #print " cmd=", cmd

         assert len(first) > 0, "TrieNode.match received a first of length 0 from util.first_token"

         node = self

         for next_char in first:
             if next_char in node.possible_next:
                 node = node.possible_next[ next_char ]
             else:
                 raise NoMatch

             if len(cmd) > 0 and node.next_token_node:
                 node.next_token_node.match( cmd )

         if node.no_abbrev:
             raise NoMatch

         #print "raising match with callback ", node.callback

         #print "raising match with first %s, remaining %s" % (first, cmd)

         cmd = cmd.lstrip()

         if len(cmd) == 0:
             cmd = None

         raise Match(node.callback, cmd)


    def __init__(self):
        self.possible_next = {}
        self.callback = None
        self.next_token_node = None
        self.no_abbrev = False


    # @todo add no_abbrev and callback data to str
    #       without breaking unit tests
    def __str__helper(self, prefix=""):
        #print "toString on TrieNode id %i with prefix %sEND" % (id(self), prefix)
        toReturn = ""

        for char in self.possible_next:
            toReturn += prefix + char + "\n"
        
        if self.next_token_node:
            assert len(prefix) > 0, "trienode.__str__ len(prefix) == 0 (no chars matched) but a next_token_node exists"
            toReturn += self.next_token_node.__str__helper( prefix + " " )
        else:
            #print "next_token_node null for prefix %s" % prefix
            pass

        for char in self.possible_next:
            toReturn += self.possible_next[char].__str__helper( prefix + char )

        return toReturn


    def __str__(self):
        return self.__str__helper()


