
import util
from trienode import TrieNode
from parser import Parser

modTrie = TrieNode()

def initMods():

    mods = util.import_libs("./mods-enabled")

    for mod in mods:
        mod.init()


def parser():
    return Parser( lambda static: [modTrie] )




    


