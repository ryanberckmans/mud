from util import first_token, toInt
from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient
from mobList import mobList
from mobTemplate import getMobTemplate, getSession
from mobTemplateForm import MobTemplateForm

def _invalidMobId( clientId, token ):
    sendToClient( clientId, "Invalid mob id '%s'" % token )

def mobEditCmd( clientId, remaining):
    if remaining:
        (token, remaining) = first_token(remaining)
        templateId = toInt(token)

        if templateId:
            mobTemplate = getMobTemplate( templateId )

            if mobTemplate:
                _editMob( clientId, mobTemplate )
                return
            
        _invalidMobId( clientId, token )

    # MobTemplateSelector
    sendToClient( clientId, "MobTemplateSelector not impl" )

def _invalidMobId( clientId, token ):
    sendToClient( clientId, "Invalid mob id '%s'" % token )

def _editMob( clientId, mobTemplate ):
    session = getSession()
    session.add( mobTemplate )
    form = MobTemplateForm( mobTemplate, session )
    form.activate( clientId )

rootCmdMap.addCmd( "mob edit", mobEditCmd )
