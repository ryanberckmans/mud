import unittest
import string
import util


class TestIsAlphanumeric(unittest.TestCase):

    def testis_alphanumeric(self):
        self.assert_( util.is_alphanumeric("abc_123"))


    def testis_not_alphanumeric(self):
        self.assert_( not util.is_alphanumeric("  yo__!!"))


class TestFirstToken(unittest.TestCase):

    def setUp(self):
        pass

    def testonly_whitespace(self):
        for char in string.whitespace:
            self.assertEquals(util.first_token( char ), ("",""))


    def testepsilon(self):
        self.assertEquals(util.first_token(""), ("",""))


    def testone_token(self):
        self.assertEquals(util.first_token("fred"), ("fred",""))


    def testremainder_no_left_whitespace(self):
        self.assertEquals(util.first_token("jim   "), ("jim",""))
        self.assertEquals(util.first_token("cast    \t\n\rfireball ted say hi omgz"), ("cast", "fireball ted say hi omgz"))
        
        
    

class TestTokenize(unittest.TestCase):

    def setUp(self):
        pass

    def testonly_whitespace(self):
        self.assertEquals( util.tokenize("\t\n\r      "), [])


    def testepsilon(self):
        self.assertEquals( util.tokenize(""), [])


    def testcorrect_num_tokens(self):
        self.assertEquals( len(util.tokenize("a b c d \t\n\rfred")), 5)


    def testcorrect_token_contents(self):
        self.assertEquals( util.tokenize("  \t\n\rfred jim \tbob   \t"), ["fred", "jim", "bob"])
