print "new cons : "
for x in _new_cons:
    print "  %i" % x

print "lost link: "
for x in _lost_link:
    print "  %i" % x

print "flushed  : "
for x in _flushed:
    print "  %i" % x

print "cmds     :"
for x in _cmds:
    print x

_cmd_router.tick( _new_cons, _lost_link, _flushed, _cmds, _msgs )

