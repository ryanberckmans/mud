from types import ListType, StringType, FunctionType
import cmdMap

def createMenu( menuPairs, defaultCallback = None ):
    """
    menuPairs: [ ( menuItemDescription, menuItemCallback ) ]
    defaultCallback: the callback executed by the menu if an invalid option is selected

    returns ( menuStr, menuMap )
      menuStr: string repr of menu to send to clients
      menuMap: CmdMap for the menu
    """

    assert type(menuPairs) == ListType, "menu.createMenu received menuPairs that wasn't a list"
    if defaultCallback:
        assert type(defaultCallback) == FunctionType, "menu.createMenu received defaultCallback that wasn't a function"

    menuStr = ""
    menuMap = CmdMap( defaultCallback )
    menuIndex = 1

    for (menuItemDescription, menuItemCallback) in menuPairs:
        assert type(menuItemDescription) == StringType, "Menu.createMenu received a menu item description that wasn't a string"
        assert type(menuItemCallback) == FunctionType, "Menu.createMenu received a menu item callback that wasn't a function"

        menuStr = menuStr + "%i) - %s\r\n" % ( menuIndex, menuItemDescription )
        menuMap.addCmd( "%i" % menuIndex, menuItemCallback)
        menuIndex += 1

    return ( menuStr, menuMap )
        
