from types import FunctionType

class AbandonCallback(Exception):

    def __init__(self, callback ):

        if callback:
            assert type(callback) == FunctionType, "parser.exceptions.AbandonCallback constructor received a non-null callback that wasn't a function"
            
        self.callback = callback
  

