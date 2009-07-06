from util import endl
from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient
from zoneTemplate import getSession, ZoneTemplate


def zoneList( clientId, remaining ):
    zoneTemplates = getSession().query(ZoneTemplate).all()

    zones = "{!{FGZone Templates:{FC" + endl
    for zt in zoneTemplates:
        zones += " " + str(zt) + endl

    sendToClient( clientId, zones )
    
        
rootCmdMap.addCmd( "zone list", zoneList )
