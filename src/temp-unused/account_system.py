import parser
from types import *
import menu
import util
import account
from account import Account


# Logon Sequence

class LogonSequence:

    def __init__( self, send_func, logon_func ):
        assert type(send_func) == FunctionType, "LogonSequence.init received send_func that wasn't a function"
        assert type(logon_func) == FunctionType, "LogonSequence.init received logon_func that wasn't a function"
        
        self.cmds = []
        self.parsers_stack = [[]]
        self.send = send_func
        self.logon = logon_func
        
        self.default_cmd_callback = None

        welcome( self )


    ### Commands ###

    def add_cmd( self, cmd ):
        assert type(cmd) == StringType, "LogonSequence.add_cmd received cmd that wasn't a string"

        self.cmds.append( cmd )


    def flush_cmds( self ):
        del self.cmds[:]


    def handle_cmd( self ):

        if len(self.cmds) > 0:

            assert len( self.parsers_stack ) > 0, "LogonSequence.handle_cmd was going to handle a cmd with an empty parsers stack"

            parser.handle_cmd( self.cmds.pop(0), self, self.parsers_stack[-1], self.default_cmd_callback )



    ### Parsers ###

    def append_parser( self, parser ):

        assert parser, "LogonSequence.append_parser received null parser"
        assert len(self.parsers_stack) > 0, "LogonSequence.append_parser detected empty parsers_stack"

        self.parsers_stack[-1].append( parser )


    def push_parsers( self, parsers ):
        assert type(parsers) == ListType, "LogonSequence.push_parsers received parsers that wasn't a list"

        self.parsers_stack.append( parsers )


    def pop_parsers( self, n = 1):  # note parsers_stack may never be empty
        assert type(n) == IntType, "LogonSequence.pop_parsers received n that wasn't an int"
        assert n > 0, "LogonSequence.pop_parsers received n that wasn't positive"

        try:
            while n > 0:
                self.parsers_stack.pop()
                n -= 1
        except IndexError:
            self.parsers_stack.append( [] ) # re-append the empty list of parsers



    # this may be temporary, it is a macro for state transitions
    def next_state( self, parser, default_cmd_callback ):
        self.pop_parsers()
        self.push_parsers( [parser] )
        self.default_cmd_callback = default_cmd_callback

        
        

# Logon Sequence "state machine" callbacks





########################################################
# Player types account name from welcome menu to login
########################################################

def logon_receive_account_name( logon_seq, account_name ):
    account_name = util.first_token(account_name)[0]
    account = get_account(account_name )
    if ( account ):
        logon_request_password( logon_seq, account )
    else:
        logon_account_doesnt_exist( logon_seq, account_name )


def logon_request_password( logon_seq, account, number_of_attempts = 1 ):
      logon_seq.send("Password:")
      logon_seq.next_state( parser.empty(), lambda diff_logon_seq, password: logon_receive_password( diff_logon_seq, password, account, number_of_attempts ) )


def logon_receive_password( logon_seq, password, account, number_of_attempts ):
    if ( password == account.password ):
        logon( logon_seq, account )
    else:
        logon_seq.send("Incorrect password.\n")
        if ( number_of_attempts > 2 ):
            #todo too many attempts, disconnect
            logon_seq.send("Too many attempts..TODO disconnect\n")

        logon_request_password( logon_seq, account, number_of_attempts + 1 )


def logon_account_doesnt_exist( logon_seq, account_name ):
    logon_seq.send("Account %s doesn't exist.\n" % account_name )
    welcome( logon_seq )
    


################################################################
# Player selects '1' from welcome menu to create a new account
################################################################

def receive_new_account_name( logon_seq, account_name):
    if ( not util.is_alphanumeric( account_name ) ):
        logon_seq.send("Account names may only contain letters, numbers, and underscores.")
        logon_input_new_account_name( logon_seq, None)
        return    
    
    if ( account_name_unused( account_name ) ):
        account = Account( account_name )
        logon_input_new_account_password( logon_seq, account )
    else:
        logon_seq.send("Account name %s already exists.\n" % account_name )
        logon_input_new_account_name( logon_seq, None )
    
def logon_input_new_account_name( logon_seq, remaining ):
    logon_seq.send("\nAccount Creation (Step 1 of 2)\nNew Account Name:")
    logon_seq.next_state( parser.empty(), receive_new_account_name )
    


################################################
# Player successfully input a new account name
################################################

def verify_new_account_password( logon_seq, account_pw, account):
    if ( account.password == account_pw ):
        account_creation_successful( logon_seq, account )
    else:
        logon_seq.send("Passwords did not match.\n")
        logon_input_new_account_password( logon_seq, account )

def receive_new_account_password( logon_seq, account_pw, account):
    if ( account_pw != util.first_token( account_pw )[0] ):
        logon_seq.send("Passwords may not have whitespace.\n")
        logon_input_new_account_password( logon_seq, account )
        return

    account.password = account_pw
    logon_seq.send("Verify Password:")
    logon_seq.next_state( parser.empty(), lambda diff_logon_seq, password: verify_new_account_password( diff_logon_seq, password, account ) )

def logon_input_new_account_password( logon_seq, account):
    logon_seq.send("Account Creation (Step 2 of 2)\nNew Account Password:")
    logon_seq.next_state( parser.empty(), lambda diff_logon_seq, password: receive_new_account_password( diff_logon_seq, password, account ) )



###################################################################
# Player successfully created a account
###################################################################

def account_creation_successful( logon_seq, account ):
    add_account( account )
    logon_seq.send("Committed your account.\n")
    logon( logon_seq, account )


###############################
# Player successfully logs on
###############################

def logon( logon_seq, account ):
    logon_seq.logon( logon_seq, account.id )


##############################
# Player connects to the MUD
##############################

welcome_menu = menu.create([("Create a New Account", logon_input_new_account_name)])

def welcome( logon_seq ):
    logon_seq.send("Welcome to MUD under development!\n\n")
    logon_seq.send( welcome_menu.str )
    logon_seq.send( "OR Account Name: " )
    logon_seq.next_state( welcome_menu.parser, logon_receive_account_name )





