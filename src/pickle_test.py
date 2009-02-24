#!/usr/bin/python

import pickle
import StringIO

from mob import Mob

s = StringIO.StringIO()

p = pickle.Pickler(s)


M = Mob(57)
M.add_cmd("HI!!!")

p.dump(M)

print( s.getvalue() )
s.close()

