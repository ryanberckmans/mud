import unittest

import util
from trienode import Match, NoMatch
import parser

class TestParser(unittest.TestCase):

    def setUp(self):
        pass


    def testinit_get_is_func(self):
        self.assertRaises(AssertionError, parser.Parser, 37)
        self.assertRaises(AssertionError, parser.Parser, "hi")


    def testparse_cmd_is_string(self):
        p = parser.Parser( lambda player: player )
        self.assertRaises(AssertionError, p.parse, 37, "player")


    def testsys_single_trie_match_works(self):
        from trienode import TrieNode
        N = TrieNode()
        N.add("jim", lambda : "jim" )

        p = parser.Parser( lambda player: [N] )
        try:
            p.parse("jim", "player")
        except Match, m:
            self.assert_(m.callback(), "jim")

    def testsys_multi_trie_match_works(self):
        from trienode import TrieNode
        N = TrieNode()
        N.add("jim", lambda : "jim" )
        Q = TrieNode()
        Q.add("fred quasar", lambda : "q" )
        p = parser.Parser( lambda player: [N, Q] )
        try:
            p.parse("f q", "player")
        except Match, m:
            self.assert_(m.callback(), "q")

    def testsys_nomatch_works(self):
         p = parser.Parser( lambda player: [] )
         self.assertRaises( NoMatch, p.parse, "fred", "player")


    
class TestHandleCmd(unittest.TestCase):

    def setUp(self):
        pass

    def testcmd_is_string(self):
        self.assertRaises(AssertionError, parser.handle_cmd, 37, "player", [], lambda : "a" )


    def testparsers_is_list(self):
        self.assertRaises(AssertionError, parser.handle_cmd, "cast fireball", "player", 37, lambda : "a" )

    def testcallback_is_function(self):
        self.assertRaises(AssertionError, parser.handle_cmd, "cast fireball", "player", [], None )

