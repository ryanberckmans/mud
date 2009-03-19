from types import StringType, FunctionType, ListType

import cmdMap

def handleCmd( cmd, client, polymorphicVariable):
    """
     handleCmd( cmd, client, polymorphic )

      - cmd: string, the cmd being handled
      - client: any type, the client executing the cmd, not used explicitly
      - polymorphic third param:
          - CmdMap, a single CmdMap
          - [CmdMap], a list of CmdMaps
          - f client -> CmdMap, a single function mapping client to a CmdMap
          - [f client -> CmdMap], a list of functions mapping client to CmdMap
    """

    assert type(cmd) == StringType, "parser.handler.handleCmd expected type(cmd)==string"
    assert client, "parser.handler.handleCmd received a null client"
    assert polymorphicVariable, "parser.handler.handleCmd received a null maps param"

    if type(polymorphicVariable) == ListType:

        if len(polymorphicVariable) == 0:
            return

        if cmdMap.isCmdMap(polymorphicVariable[0]):
            handleCmdFromMaps( cmd, client, polymorphicVariable)
        else:
            assert type(polymorphicVariable[0]) == FunctionType, "parser.handler.handleCmd received a list and it did not contain CmdMaps or functions"
            handleCmdFromAccessors( cmd, client, polymorphicVariable)

    else:
        if cmdMap.isCmdMap(polymorphicVariable):
            handleCmdFromMap( cmd, client, polymorphicVariable)
        else:
            assert type(polymorphicVariable) == FunctionType, "parser.handler.handleCmd received a single object and it wasn't a CmdMap or function"
            handleCmdFromAccessor( cmd, client, polymorphicVariable)
            

###################################
## Internal #######################
###################################

def handleCmdFromAccessor( cmd, client, cmdMapAccessor):
    handleCmdFromMaps( cmd, client, [cmdMapAccessor( client )] )

def handleCmdFromAccessors( cmd, client, cmdMapAccessors ):
    cmdMaps = map( lambda x: x( client ), cmdMapAccessors )
    handleCmdFromMaps( cmdMaps )

def handleCmdFromMaps( cmd, client, cmdMaps ):
    abandonedCallback = None

    for cmdMap in cmdMaps:
        assert CmdMap.isCmdMap( cmdMap ), "parser.handler.handleCmd; cmdMaps list contains a non-CmdMap"
        (callback, remaining) = cmdMap.find( cmd )

        if callback:
            try:
                callback( client, remaining)
            except AbandonCallback, e:
                abandonedCallback = e.callback

            return # handled!

    if abandonedCallback:
        abandonedCallback( client )

    return # handled!

