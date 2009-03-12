import unittest

from .. import trie, exceptions

def a():
    return "a"

def b():
    return "b"

def c():
    return "c"


class TestTrie(unittest.TestCase):
    
    def setUp(self):
        self.node = trie.CmdMap()

    def testrepr(self):
        self.assertEqual(str(self.node), "")
        self.node.addCmd( "abc", a )
        self.assertEqual( str(self.node), "a\nab\nabc\n")

    
    def testadd_cmd_is_string(self):
        self.assertRaises(AssertionError, self.node.addCmd, None, a)
        self.assertRaises(AssertionError, self.node.addCmd, 17, a)

    def testadd_callback_is_function(self):
        self.assertRaises(AssertionError, self.node.addCmd, "Jim", None)
        self.assertRaises(AssertionError, self.node.addCmd, "Jim", 17)

    def testadd_noabbrev_is_bool(self):
        self.assertRaises(AssertionError, self.node.addCmd, "jim", a, None)
        self.assertRaises(AssertionError, self.node.addCmd, "jim", a, 17)

    def testadd_returnsself(self):
        self.assert_(self.node == self.node.addCmd("jim", a))

    def testmatch_cmd_is_string(self):
        self.assertRaises(AssertionError, self.node.match, None)
        self.assertRaises(AssertionError, self.node.match, 17)

    def testsys_epsilon_nomatch(self):
        self.assertRaises(exceptions.NoMatch, self.node.match, "")

    def testsys_single_match(self):
        self.node.addCmd( "abc", a )
        self.assertRaises(exceptions.Match, self.node.match, "abc")

    def testsys_all_prefixes_match(self):
        self.node.addCmd( "abc", a )
        self.assertRaises(exceptions.Match, self.node.match, "a")
        self.assertRaises(exceptions.Match, self.node.match, "ab")

    def testsys_callback_works(self):
        self.node.addCmd( "abc", a )
        try:
            self.node.match("abc")
        except exceptions.Match, m:
            self.assert_(m.callback() == "a")

    def testsys_multitoken_match(self):
        self.node.addCmd( "cast fireball", a )
        self.assertRaises(exceptions.Match, self.node.match, "cast fireball")


    def testsys_all_prefixes_multitoken_match(self):
        self.node.addCmd( "cast fly", a )
        self.assertRaises(exceptions.Match, self.node.match, "c fly")
        self.assertRaises(exceptions.Match, self.node.match, "ca fly")
        self.assertRaises(exceptions.Match, self.node.match, "cas fly")
        self.assertRaises(exceptions.Match, self.node.match, "cast f")
        self.assertRaises(exceptions.Match, self.node.match, "cast fl")
        self.assertRaises(exceptions.Match, self.node.match, "cas  f")
        self.assertRaises(exceptions.Match, self.node.match, "cas  fl")
        self.assertRaises(exceptions.Match, self.node.match, "cas  fly")
        self.assertRaises(exceptions.Match, self.node.match, "ca  f")
        self.assertRaises(exceptions.Match, self.node.match, "ca  fl")
        self.assertRaises(exceptions.Match, self.node.match, "ca  fly")
        self.assertRaises(exceptions.Match, self.node.match, "c  f")
        self.assertRaises(exceptions.Match, self.node.match, "c  fl")
        self.assertRaises(exceptions.Match, self.node.match, "c  fly")

    def testsys_overwrite_match(self):
        self.node.addCmd( "abc", a )
        self.node.addCmd( "abc", b )
        try:
            self.node.match("abc")
        except exceptions.Match, m:
            self.assert_(m.callback() == "a")

    def testsys_longer_match(self):
        self.node.addCmd( "abc", a )
        self.node.addCmd( "abcd", b )
        try:
            self.node.match("abcd")
        except exceptions.Match, m:
            self.assert_(m.callback() == "b")

    def testsys_greedy_match(self):
        self.node.addCmd( "abc", a )
        self.node.addCmd( "abc def", b )
        try:
            self.node.match("abc def")
        except exceptions.Match, m:
            self.assert_(m.callback() == "b")
        
    def testsys_noabbrev_match(self):
        self.node.addCmd( "abc", a, True )
        self.assertRaises(exceptions.NoMatch, self
                          .node.match, "a")
        self.assertRaises(exceptions.NoMatch, self.node.match, "ab")
        self.assertRaises(exceptions.Match, self.node.match, "abc")

    def testsys_noabbrev_overwrite_match(self):
        self.node.addCmd( "abc", a, True )
        self.node.addCmd( "abc", b, True )
        self.assertRaises(exceptions.NoMatch, self.node.match, "a")
        self.assertRaises(exceptions.NoMatch, self.node.match, "ab")
        try:
            self.node.match("abc")
        except exceptions.Match, m:
            self.assert_(m.callback() == "a")

    def testsys_noabbrev_overwrite_longer_match(self):
        self.node.addCmd( "abc", a, True )
        self.node.addCmd( "abcd", b, True )
        self.assertRaises(exceptions.NoMatch, self.node.match, "a")
        self.assertRaises(exceptions.NoMatch, self.node.match, "ab")
        try:
            self.node.match("abc")
        except exceptions.Match, m:
            self.assert_(m.callback() == "a")
        try:
            self.node.match("abcd")
        except exceptions.Match, m:
            self.assert_(m.callback() == "b")

     
