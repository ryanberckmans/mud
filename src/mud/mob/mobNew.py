from mud.core.rootCmdMap import rootCmdMap
from mobTemplate import MobTemplate, getSession
from mobTemplateForm import MobTemplateForm

def mobNewCmd( clientId, remaining ):
    template = MobTemplate()
    session = getSession()
    session.add(template)
    form = MobTemplateForm( template, session )
    form.activate( clientId )    

rootCmdMap.addCmd( "mob new", mobNewCmd )
