from types import ListType, StringType, FunctionType
from parser import Parser
from trienode import TrieNode

# items is a list of (string, callback)
def create( items ):

    assert( type(items) == ListType ), "Menu.create received items that wasn't a list"

    menu_str = ""
    menu_trienode = TrieNode()

    menu_index = 1
    for item in items:

        assert type(item[0]) == StringType, "Menu.create received an item[0] that wasn't a string"
        assert type(item[1]) == FunctionType, "Menu.create received an item[1] that wasn't a function"
        
        menu_str = menu_str + "%i) - %s\n" % (menu_index, item[0])
        menu_trienode.add( "%i" % menu_index, item[1] )

        menu_index += 1


    return Menu( menu_str, Parser( lambda unused: [menu_trienode] ) )

    
    
class Menu:

    def __init__(self, string, parser):
        self.str = string
        self.parser = parser
       
