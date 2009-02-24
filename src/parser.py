import types

import util
from trienode import NoMatch, Match

class Parser:

    def __init__(self, get):
        assert type(get) == types.FunctionType
        self.get = get


    def parse( self, cmd, player ):

        assert type(cmd) == types.StringType, "Parser.parse received cmd that wasn't a string"

        tries = self.get( player )

        for trie in tries:
            try:
                trie.match( cmd )
            except NoMatch:
                pass
            
        raise NoMatch
    


# returns an empty parser
def empty():
    return Parser( lambda player: [] )

    

# cmd - string
# player - the player who's command this is
# parsers - list of Parser objects
# callback - default NoMatch fnct /w signature( player, cmd )
# always returns
def handle_cmd( cmd, player, parsers, callback ):

    assert type(cmd) == types.StringType, "parser.handle_cmd received cmd that wasn't a string"
    assert type(parsers) == types.ListType, "parser.handle_cmd received parsers that wasn't a list"
    assert type(callback) == types.FunctionType, "parser.handle_cmd received callback that wasn't a function"
  
    keyword = None
    nokeywordmatch = False

    for parser in parsers:

        try:
            parser.parse( cmd, player )
        except NoMatch:
            continue
        except Match, m:

            try:
                assert m.callback, "parser.handle_cmd received null callback while handling Match"
                m.callback( player, m.remaining)
                return # handled!

            except NoKeywordMatch, m:

                callback = m.callback
                keyword = m.keyword

                nokeywordmatch = True

                assert type(callback) == types.FunctionType, "parser.handle_cmd received callback that wasn't a function while handling NoKeywordMatch"
                assert type(keyword) == types.StringType, "parser.handle_cmd received keyword that wasn't a string while handling NoKeywordMatch"


    if nokeywordmatch:
        callback( player, keyword) # handle NoKeywordMatch
    else:
        callback( player, cmd ) # handle NoMatch


# Parser Exceptions

class NoKeywordMatch(Exception):

    def __init__(self, callback, keyword):

        assert callback, "NoKeywordMatch constructor received null callback"

        self.callback = callback
        self.keyword = keyword

    def __str__(self):

        return "NoKeywordMatch with keyword " + keyword
  

