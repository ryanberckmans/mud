import mud.parser.cmdMap as cmdMap
import mud.parser.handler as handler

t = cmdMap.CmdMap()

def s( q):
    def p( client, remaining ):
        print "you casted the spell %s (remaining: %s)" % (q, remaining)
        None
    t.addCmd("cast %s" % q, p )

s("fireball")
s("fly")
s("frigid blizzard")

import sys
while 1:
    line = sys.stdin.readline()
    handler.handleCmd( line, "client", t )
    
