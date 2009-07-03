import string
import re
import os, sys, inspect
from types import *
import cppTypes

endl = "\r\n"

def toCpp( obj ):
    if type(obj) == list:
        if len(obj) == 0:
            return cppIntVector()
        if type(obj[0]) == float or type(obj[0]) == int:
            vec = cppDoubleVector()
            vec.extend( obj )
            return vec


def newlines( i ):
    return newline( i )

def newline( i ):
    isInt( i )
    assert i > -1
    nls = ""
    for j in range(0, i+1):
        nls += "\r\n"
    return nls


def typeCheck( s, t ):
    if ( type(s) == t ):
        return True
    return False

def isBool( s ):
    return typeCheck( s, BooleanType )

def isTuple( s ):
    return typeCheck( s, TupleType )

def isDefined( s ):
    return s != None

def isString( s ):
    return typeCheck( s, StringType )

def isStr( s ): return isString( s )

def isFunc( s ):
    assert type(s) == FunctionType
    return True

def isFunction( s ): return isFunc (s)

def isDict( s ):
    assert type(s) == DictType
    return True

def isInt( s ):
    assert type(s) == IntType
    return True

def isFloat( s ):
    assert type(s) == FloatType or isInt( s )
    return True

def isList( s ):
    assert type(s) == ListType
    return True


# returns true if str contains only alphanumeric + underscore

isAlphanumericExp = re.compile('.*\W.*')
def is_alphanumeric( str ):
    return isAlphanumericExp.match( str ) == None


# returns the first token delimited by a space or a tab
def first_token( str ):
    str = str.lstrip()

    assert len(str) or len(str) == 0  # just check to make sure len(str) exists

    if len(str) == 0:
        return ("", "")
    
    index = 0

    for char in str:

        if char in string.whitespace:
            break

        index +=1

    #print "index ", index
    #print str[:index]

    return (str[:index], str[index:].lstrip())

# remember, it is unsafe to call tokenize on raw user input :)
def tokenize( str ):

    if len(str.lstrip()) == 0:
        return []
    
    tokens = []

    while 1:
        (token, str) = first_token( str )

        assert len(token) > 0, "util.tokenize received a token of length 0 from first_token"

        tokens.append(token)

        if len(str) == 0:
            break

    return tokens


########################
# list contents of dir
########################

def ls( dir ):
    return os.listdir(os.path.abspath(dir))
    

########################
# dynamic module loader
########################

"""
loader.py - From a directory name:

1: append the directory to the sys.path
2: find all modules within that directory
3: import all modules within that directory
4: filter out built in methods from those modules
5: return a list of useable methods from those modules

Allows the user to import a series of python modules without "knowing" anything
about those modules.

Copyright 2005 Jesse Noller <jnoller@gmail.com>

"""

def import_libs(dir):
    """ Imports the libs, returns a list of the libraries. 
    Pass in dir to scan """
    
    library_list = []

    for f in os.listdir(os.path.abspath(dir)):       
        module_name, ext = os.path.splitext(f) # Handles no-extension files, etc.
        if ext == '.py': # Important, ignore .pyc/other files.
            print 'imported module: %s' % (module_name)
            module = __import__(module_name)
            library_list.append(module)
 
    return library_list




#####################################
# below are from Peter Norvig's util
#####################################

def abstract():
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')


class Struct:
    """Create an instance with argument=value slots.
    This is for making a lightweight object whose class doesn't matter."""
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __cmp__(self, other):
        if isinstance(other, Struct):
            return cmp(self.__dict__, other.__dict__)
        else:
            return cmp(self.__dict__, other)

    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)

def probability(p):
    import random
    "Return true with probability p."
    return p > random.uniform(0.0, 1.0)
