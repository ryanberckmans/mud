import unittest

from mob import Mob


class TestMob(unittest.TestCase):


    def setUp(self):
        self.mob = Mob( 57 )
        pass

    def testid_works(self):
        self.assert_(self.mob.ID == 57)

    def testno_prompt_yields_epsilon(self):
        self.assert_(self.mob.prompt() == "")

    def testpush_prompt_works(self):
        self.mob.push_prompt( lambda mob: ":D" )
        self.assert_(self.mob.prompt() == ":D")

    def testpop_prompt_works(self):
         self.mob.push_prompt( lambda mob: ":D" )
         self.mob.push_prompt( lambda mob: ":|" )
         self.mob.pop_prompt()
         pr = self.mob.prompt()
         print "prompt: %s", pr
         self.assert_(self.mob.prompt() == ":D")
         self.mob.push_prompt( lambda mob: "a" )
         self.mob.push_prompt( lambda mob: "b" )
         self.mob.push_prompt( lambda mob: "c" )
         self.mob.pop_prompt(2)
         self.assert_(self.mob.prompt() == "a")
         self.mob.pop_prompt(500)
       
    def testpop_prompt_neg_asserts(self):
        self.assertRaises(AssertionError, self.mob.pop_prompt, -1)

    def testadd_cmd_works(self):
        self.assert_(len(self.mob.cmds) == 0)
        self.mob.add_cmd("castfireball!!")
        self.assert_(len(self.mob.cmds) == 1)

    def testflush_cmds_works(self):
        self.mob.add_cmd("castfireball!!")
        self.mob.flush_cmds()
        self.assert_(len(self.mob.cmds) == 0)


      

        

        
