from pydispatch import dispatcher

def connect( callback, signal ):
    dispatcher.connect( callback, signal )


## HACK - use Classes for signals now

class CONNECTED:
    def __init__( self ):
        pass

class DISCONNECTED:
    def __init__( self ):
        pass

class BEFORE_TICK:
    def __init__( self ):
        pass

class AFTER_TICK:
    def __init__( self ):
        pass



    
