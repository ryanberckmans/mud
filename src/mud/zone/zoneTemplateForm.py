from util import isDefined, endl
from mud.menu.form import Form
from mud.core.cmds import popCmdHandler
from mud.core.prompt import popPrompt

def finishCallback( clientId, session, abort = False ):

    if ( abort ):
        session.rollback()
    else:
        session.commit()

    session.close()

    popCmdHandler( clientId )
    popPrompt( clientId )

class ZoneTemplateForm:

    def __init__( self, zoneTemplate, session ):
        assert isDefined( zoneTemplate )
        assert isDefined( session )

        assert zoneTemplate in session

        self.zoneTemplate = zoneTemplate
        self.session      = session

        title = endl + "{FYEditing "
        if zoneTemplate.id:
            title += "Zone " + zoneTemplate.id
        else:
            title += "New Zone"
        
        menuItems = [
            title,
            ( "Zone Name", lambda x:x, lambda clientId: self.zoneTemplate.name )
            ]

        self.form = Form( menuItems, lambda clientId, abort=False: finishCallback( clientId, session, abort ) )
        self.form.prompt = endl + "{!{FB<select an option>"

    def activate( self, clientId ):
        self.form.activate( clientId )
