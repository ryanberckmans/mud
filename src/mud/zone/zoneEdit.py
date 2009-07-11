from util import first_token, toInt
from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient
from zoneList import zoneList
from zoneTemplate import getZoneTemplate

def _invalidZoneId( clientId, token ):
    sendToClient( clientId, "Invalid zone id '%s'" % token )

def zoneEditCmd( clientId, remaining):
    if remaining:
        (token, remaining) = first_token(remaining)
        templateId = toInt(token)

        if templateId:
            zone = getZoneTemplate( templateId )

            if zone:
                _editSpecificZone( clientId, templateId )
                return
            
        _invalidZoneId( clientId, token )

    # ZoneTemplateSelector
    pass

def _invalidZoneId( clientId, token ):
    sendToClient( clientId, "Invalid zone id '%s'" % token )

def _editSpecificZone( clientId, zoneTemplate ):
    sendToClient( clientId, "Tried to edit %s" % str(zoneTemplate) )

rootCmdMap.addCmd( "zone edit", zoneEditCmd )
