from client import Client
import mod

class CmdRouter:

    def __init__(self):
        self.idMap = {}
        mod.initMods()


    def tick( self, new_cons, lost_link, flushed, cmds, msgs):

        # TODO crash bug edge case, what if someone connections then lls in the same pulse?
        # First process lost links
        for con in lost_link:
            assert con in self.idMap, "CmdRouter.tick received a ll con id that wasn't in the con map"

            del self.idMap[con]
            # todo send ll to game


        print "after ll"
        print str(self.idMap)


        # Second process new connections
        for con in new_cons:
            assert con not in self.idMap, "CmdRouter.tick received a new con id that was already in the con map"

            def send(msg):
                if con in msgs:
                    msgs[con] = msgs[con] + msg
                else:
                    msgs[con] = msg


            self.idMap[con] = Client( send, mod.parser() )

        print "after new"
        print str(self.idMap)

        # Third flush cmd queues
        for con in flushed:
            assert con in self.idMap, "CmdRouter.tick received a flushed con id that wasn't in the con map"

            self.idMap[con].flushCmds()

        print "after flush"
        print str(self.idMap)

        # Fourth add new cmds
        for cmd in cmds:
            print "cmd key %i " % cmd.key()
            print "cmd data %s " % cmd.data()
            assert cmd.key() in self.idMap, "CmdRouter.tick received a cmd for a con id that wasn't in the con map"
            self.idMap[cmd.key()].addCmd(cmd.data())


        # Handle commands for all connections
        for con in self.idMap:
            self.idMap[con].handleCmd()

        

        


