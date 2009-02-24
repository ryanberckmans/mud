from account_system import LogonSequence

class CmdRouter:

    def __init__(self):
        self.id_map = {}


    def tick( self, new_cons, lost_link, flushed, cmds, msgs):

        # TODO crash bug edge case, what if someone connections then lls in the same pulse?
        # First process lost links
        for con in lost_link:
            assert con in self.id_map, "CmdRouter.tick received a ll con id that wasn't in the con map"

            del self.id_map[con]
            # todo send ll to game


        print "after ll"
        print str(self.id_map)


        # Second process new connections
        for con in new_cons:
            assert con not in self.id_map, "CmdRouter.tick received a new con id that was already in the con map"

            def send(msg):
                if con in msgs:
                    msgs[con] = msgs[con] + msg
                else:
                    msgs[con] = msg


            def logon( logon_seq, account_id ):
                logon_seq.send("Logged in!")
                

            self.id_map[con] = LogonSequence( send, logon )

        print "after new"
        print str(self.id_map)

        # Third flush cmd queues
        for con in flushed:
            assert con in self.id_map, "CmdRouter.tick received a flushed con id that wasn't in the con map"

            self.id_map[con].flush_cmds()

        print "after flush"
        print str(self.id_map)

        # Fourth add new cmds
        for cmd in cmds:
            print "cmd key %i " % cmd.key()
            print "cmd data %s " % cmd.data()
            assert cmd.key() in self.id_map, "CmdRouter.tick received a cmd for a con id that wasn't in the con map"
            self.id_map[cmd.key()].add_cmd(cmd.data())


        # Handle commands for all connections
        for con in self.id_map:
            self.id_map[con].handle_cmd()

        

        


