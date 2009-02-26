
import mod


def cmdTest( client, remaining ):
    client.send("You executed the cmd 'test', remaining: %s\n" % remaining )

def init():
    mod.modTrie.add( "test", cmdTest )
    
