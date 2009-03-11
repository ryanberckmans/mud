import unittest

from .. import trie
#from ..exceptions import Match, NoMatch

def a():
    return "a"

def b():
    return "b"

def c():
    return "c"


class TestTrie(unittest.TestCase):
    
    def setUp(self):
        self.node = trie.Trie()

    def testrepr(self):
        self.assertEqual(str(self.node), "")
        self.node.add( "abc", a )
        self.assertEqual( str(self.node), "a\nab\nabc\n")

    
    def testadd_cmd_is_string(self):
        self.assertRaises(AssertionError, self.node.add, None, a)
        self.assertRaises(AssertionError, self.node.add, 17, a)

    def testadd_callback_is_function(self):
        self.assertRaises(AssertionError, self.node.add, "Jim", None)
        self.assertRaises(AssertionError, self.node.add, "Jim", 17)

    def testadd_noabbrev_is_bool(self):
        self.assertRaises(AssertionError, self.node.add, "jim", a, None)
        self.assertRaises(AssertionError, self.node.add, "jim", a, 17)

    def testadd_returnsself(self):
        self.assert_(self.node == self.node.add("jim", a))

    def testmatch_cmd_is_string(self):
        self.assertRaises(AssertionError, self.node.match, None)
        self.assertRaises(AssertionError, self.node.match, 17)

    def testsys_epsilon_nomatch(self):
        self.assertRaises(trienode.NoMatch, self.node.match, "")

    def testsys_single_match(self):
        self.node.add( "abc", a )
        self.assertRaises(trienode.Match, self.node.match, "abc")

    def testsys_all_prefixes_match(self):
        self.node.add( "abc", a )
        self.assertRaises(trienode.Match, self.node.match, "a")
        self.assertRaises(trienode.Match, self.node.match, "ab")

    def testsys_callback_works(self):
        self.node.add( "abc", a )
        try:
            self.node.match("abc")
        except trienode.Match, m:
            self.assert_(m.callback() == "a")

    def testsys_multitoken_match(self):
        self.node.add( "cast fireball", a )
        self.assertRaises(trienode.Match, self.node.match, "cast fireball")


    def testsys_all_prefixes_multitoken_match(self):
        self.node.add( "cast fly", a )
        self.assertRaises(trienode.Match, self.node.match, "c fly")
        self.assertRaises(trienode.Match, self.node.match, "ca fly")
        self.assertRaises(trienode.Match, self.node.match, "cas fly")
        self.assertRaises(trienode.Match, self.node.match, "cast f")
        self.assertRaises(trienode.Match, self.node.match, "cast fl")
        self.assertRaises(trienode.Match, self.node.match, "cas  f")
        self.assertRaises(trienode.Match, self.node.match, "cas  fl")
        self.assertRaises(trienode.Match, self.node.match, "cas  fly")
        self.assertRaises(trienode.Match, self.node.match, "ca  f")
        self.assertRaises(trienode.Match, self.node.match, "ca  fl")
        self.assertRaises(trienode.Match, self.node.match, "ca  fly")
        self.assertRaises(trienode.Match, self.node.match, "c  f")
        self.assertRaises(trienode.Match, self.node.match, "c  fl")
        self.assertRaises(trienode.Match, self.node.match, "c  fly")

    def testsys_overwrite_match(self):
        self.node.add( "abc", a )
        self.node.add( "abc", b )
        try:
            self.node.match("abc")
        except trienode.Match, m:
            self.assert_(m.callback() == "a")

    def testsys_longer_match(self):
        self.node.add( "abc", a )
        self.node.add( "abcd", b )
        try:
            self.node.match("abcd")
        except trienode.Match, m:
            self.assert_(m.callback() == "b")

    def testsys_greedy_match(self):
        self.node.add( "abc", a )
        self.node.add( "abc def", b )
        try:
            self.node.match("abc def")
        except trienode.Match, m:
            self.assert_(m.callback() == "b")
        
    def testsys_noabbrev_match(self):
        self.node.add( "abc", a, True )
        self.assertRaises(trienode.NoMatch, self
                          .node.match, "a")
        self.assertRaises(trienode.NoMatch, self.node.match, "ab")
        self.assertRaises(trienode.Match, self.node.match, "abc")

    def testsys_noabbrev_overwrite_match(self):
        self.node.add( "abc", a, True )
        self.node.add( "abc", b, True )
        self.assertRaises(trienode.NoMatch, self.node.match, "a")
        self.assertRaises(trienode.NoMatch, self.node.match, "ab")
        try:
            self.node.match("abc")
        except trienode.Match, m:
            self.assert_(m.callback() == "a")

    def testsys_noabbrev_overwrite_longer_match(self):
        self.node.add( "abc", a, True )
        self.node.add( "abcd", b, True )
        self.assertRaises(trienode.NoMatch, self.node.match, "a")
        self.assertRaises(trienode.NoMatch, self.node.match, "ab")
        try:
            self.node.match("abc")
        except trienode.Match, m:
            self.assert_(m.callback() == "a")
        try:
            self.node.match("abcd")
        except trienode.Match, m:
            self.assert_(m.callback() == "b")

     
