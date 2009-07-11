from util import endl
from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient
from zoneTemplate import getSession, ZoneTemplate


def zoneListCmd( clientId, remaining ):
    zoneTemplates = zoneList()

    zones = "{!{FGZone Templates:{FC" + endl
    for zt in zoneTemplates:
        zones += " " + str(zt) + endl

    sendToClient( clientId, zones )
    
def zoneList():
    session = getSession()
    zoneTemplates = session.query(ZoneTemplate).all()
    session.close()
    return zoneTemplates

rootCmdMap.addCmd( "zone list", zoneListCmd )



