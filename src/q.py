import mud
from mud.parser.trie import CmdMap ; t = CmdMap() ;

t.addCmd("say hi", lambda:"say hi")
t.addCmd("cast fireball", lambda:"fireball")
t.addCmd("cast fizz", lambda:"fizz")


def run( cmd ):
    try:
        t.map( cmd )
    except mud.parser.exceptions.Match, m:
        print "f: %s   remain: %s" % (m.callback(), m.remaining)
    except mud.parser.exceptions.NoMatch:
        print "NoMatch"
