#!/usr/bin/python

from mob import *
from trienode import *
from parser import *

def fireball( mob, remaining):
    print "mob id %i" % mob.ID
    print "remaining %s" % remaining
    print "FIREBALL!!!!"

N = TrieNode()
N.add("cast fireball", fireball)

P = Parser( lambda static: [N] )

M = Mob(87)

M.append_parser( P )

M.add_cmd("invalid!")
M.add_cmd("ca fi jon")
M.handle_cmd()
M.handle_cmd()
M.push_prompt( lambda mob: "%i>" % mob.ID )
print (M.prompt() )


