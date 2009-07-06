from util import first_token, toInt
from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient

def _invalidZoneId( clientId, token ):
    sendToClient( clientId, "Invalid zone id '%s'" % token )

def zoneEdit( clientId, remaining):
    session = getSession()
    
    zone = None
    if remaining:
        token = first_token(remaining)
        templateId = toInt(token)

        if templateId:
            zone = session.query(ZoneTemplate).filter(ZoneTemplate.id == templateId ).first()

            if not zone:
                _invalidZoneId( clientId, token )
                return
        else:
            _invalidZoneId( clientId, token )
            return


rootCmdMap.addCmd( "zone edit", zoneEdit )
