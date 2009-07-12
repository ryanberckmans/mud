from util import endl
from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient
from mobTemplate import getSession, MobTemplate


def mobListCmd( clientId, remaining ):
    mobTemplates = mobList()

    mobs = "{!{FGMob Templates:{FC" + endl
    for mt in mobTemplates:
        mobs += " " + str(mt) + endl

    sendToClient( clientId, mobs )
    
def mobList():
    session = getSession()
    mobTemplates = session.query(MobTemplate).all()
    session.close()
    return mobTemplates

rootCmdMap.addCmd( "mob list", mobListCmd )



