import unittest

import keywordset


class TestKeywordSet(unittest.TestCase):

    def setUp(self):
        self.set = keywordset.KeywordSet()


    def testempty_add_has(self):
        self.set.add("george")

        self.assert_(self.set.has("g"))
        self.assert_(self.set.has("ge"))
        self.assert_(self.set.has("geo"))
        self.assert_(self.set.has("geor"))
        self.assert_(self.set.has("georg"))
        self.assert_(self.set.has("george"))


    def testempty_has(self):
        self.assert_( not self.set.has("george"))


    def testadd_same_twice(self):
        self.assert_(self.set.add("ogre"))
        self.assert_(not self.set.add("ogre"))

    def testadd_diff(self):
        self.assert_(self.set.add("george"))
        self.assert_(self.set.add("fred"))
        self.assert_(self.set.add("georgeo"))

    def testhas_epsilon(self):
        self.assert_(not self.set.has(""))

    def testhas_not_single_token(self):
        self.set.add("jim")
        self.assert_(not self.set.has("jim "))

    def testhas_overshoot(self):
        self.set.add("jim")
        self.assert_(not self.set.has("jimb"))

    def testadd_epsilon(self):
        self.assert_(not self.set.add(""))

    def testadd_multitoken_fails(self):
        self.assert_(not self.set.add("jim fred"))


        
        
        

        

    
