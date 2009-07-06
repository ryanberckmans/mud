from mud.core.rootCmdMap import rootCmdMap
from zoneTemplate import ZoneTemplate, getSession
from zoneTemplateForm import ZoneTemplateForm

def zoneNew( clientId, remaining ):
    zt = ZoneTemplate()
    session = getSession()
    session.add(zt)
    form = ZoneTemplateForm( zt, session )
    form.activate( clientId )    

rootCmdMap.addCmd( "zone new", zoneNew )
