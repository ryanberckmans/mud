 
# cmd - string
# player - the player who's command this is
# parsers - list of Parser objects
# callback - default NoMatch fnct /w signature( player, cmd )
# always returns
def handleCmd( cmd, player, parsers, callback ):

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

