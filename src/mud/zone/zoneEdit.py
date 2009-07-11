from util import first_token, toInt
from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient
from zoneList import zoneList
from zoneTemplate import getZoneTemplate, getSession
from zoneTemplateForm import ZoneTemplateForm

def _invalidZoneId( clientId, token ):
    sendToClient( clientId, "Invalid zone id '%s'" % token )

def zoneEditCmd( clientId, remaining):
    if remaining:
        (token, remaining) = first_token(remaining)
        templateId = toInt(token)

        if templateId:
            zoneTemplate = getZoneTemplate( templateId )

            if zoneTemplate:
                _editZone( clientId, zoneTemplate )
                return
            
        _invalidZoneId( clientId, token )

    # ZoneTemplateSelector
    pass

def _invalidZoneId( clientId, token ):
    sendToClient( clientId, "Invalid zone id '%s'" % token )

def _editZone( clientId, zoneTemplate ):
    session = getSession()
    session.add( zoneTemplate )
    form = ZoneTemplateForm( zoneTemplate, session )
    form.activate( clientId )

rootCmdMap.addCmd( "zone edit", zoneEditCmd )
