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
        self.assertRaises(AssertionError, self.node.map, None)
        self.assertRaises(AssertionError, self.node.map, 17)

    def testsys_epsilon_nomatch(self):
        self.assertRaises(exceptions.NoMatch, self.node.map, "")

    def testsys_single_match(self):
        self.node.addCmd( "abc", a )
        self.assertRaises(exceptions.Match, self.node.map, "abc")

    def testsys_all_prefixes_match(self):
        self.node.addCmd( "abc", a )
        self.assertRaises(exceptions.Match, self.node.map, "a")
        self.assertRaises(exceptions.Match, self.node.map, "ab")

    def testsys_callback_works(self):
        self.node.addCmd( "abc", a )
        try:
            self.node.map("abc")
        except exceptions.Match, m:
            self.assert_(m.callback() == "a")

    def testsys_multitoken_match(self):
        self.node.addCmd( "cast fireball", a )
        self.assertRaises(exceptions.Match, self.node.map, "cast fireball")


    def testsys_all_prefixes_multitoken_match(self):
        self.node.addCmd( "cast fly", a )
        self.assertRaises(exceptions.Match, self.node.map, "c fly")
        self.assertRaises(exceptions.Match, self.node.map, "ca fly")
        self.assertRaises(exceptions.Match, self.node.map, "cas fly")
        self.assertRaises(exceptions.Match, self.node.map, "cast f")
        self.assertRaises(exceptions.Match, self.node.map, "cast fl")
        self.assertRaises(exceptions.Match, self.node.map, "cas  f")
        self.assertRaises(exceptions.Match, self.node.map, "cas  fl")
        self.assertRaises(exceptions.Match, self.node.map, "cas  fly")
        self.assertRaises(exceptions.Match, self.node.map, "ca  f")
        self.assertRaises(exceptions.Match, self.node.map, "ca  fl")
        self.assertRaises(exceptions.Match, self.node.map, "ca  fly")
        self.assertRaises(exceptions.Match, self.node.map, "c  f")
        self.assertRaises(exceptions.Match, self.node.map, "c  fl")
        self.assertRaises(exceptions.Match, self.node.map, "c  fly")

    def testsys_overwrite_match(self):
        self.node.addCmd( "abc", a )
        self.node.addCmd( "abc", b )
        try:
            self.node.map("abc")
        except exceptions.Match, m:
            self.assert_(m.callback() == "a")

    def testsys_longer_match(self):
        self.node.addCmd( "abc", a )
        self.node.addCmd( "abcd", b )
        try:
            self.node.map("abcd")
        except exceptions.Match, m:
            self.assert_(m.callback() == "b")

    def testsys_greedy_match(self):
        self.node.addCmd( "abc", a )
        self.node.addCmd( "abc def", b )
        try:
            self.node.map("abc def")
        except exceptions.Match, m:
            self.assert_(m.callback() == "b")
        
    def testsys_noabbrev_match(self):
        self.node.addCmd( "abc", a, False )
        self.assertRaises(exceptions.NoMatch, self
                          .node.map, "a")
        self.assertRaises(exceptions.NoMatch, self.node.map, "ab")
        self.assertRaises(exceptions.Match, self.node.map, "abc")

    def testsys_noabbrev_overwrite_match(self):
        self.node.addCmd( "abc", a, False )
        self.node.addCmd( "abc", b, False )
        self.assertRaises(exceptions.NoMatch, self.node.map, "a")
        self.assertRaises(exceptions.NoMatch, self.node.map, "ab")
        try:
            self.node.map("abc")
        except exceptions.Match, m:
            self.assert_(m.callback() == "a")

    def testsys_noabbrev_overwrite_longer_match(self):
        self.node.addCmd( "abc", a, False )
        self.node.addCmd( "abcd", b, False )
        self.assertRaises(exceptions.NoMatch, self.node.map, "a")
        self.assertRaises(exceptions.NoMatch, self.node.map, "ab")
        try:
            self.node.map("abc")
        except exceptions.Match, m:
            self.assert_(m.callback() == "a")
        try:
            self.node.map("abcd")
        except exceptions.Match, m:
            self.assert_(m.callback() == "b")

     
