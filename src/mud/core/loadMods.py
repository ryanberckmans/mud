import util

mods = util.ls("./mods-enabled")

for mod in mods:
    __import__(mod)
    print "imported mod %s" % mod
