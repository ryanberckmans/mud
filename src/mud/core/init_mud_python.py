import cmd_router


# Socket Data mapped to C++
_new_cons = IntVector()
_lost_link = IntVector()
_flushed = IntVector()
_cmds = IntStringMap()
_msgs = IntStringMap() # Outbound

_cmd_router = cmd_router.CmdRouter()
