
import util
from trienode import TrieNode
from parser import Parser

modTrie = TrieNode()

def init():

    mods = util.ls("./mods-enabled")

    for mod in mods:
        __import__(mod)
        print "imported mod %s" % mod


def parser():
    return Parser( lambda static: [modTrie] )




    


