from util import isDefined, endl
from mud.menu.form import Form
from mud.menu.textInput import getOneLine
from mud.core.cmds import popCmdHandler
from mud.core.prompt import popPrompt, pushPrompt
from mud.core.send import sendToClient

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
            ( "Zone Name", lambda clientId: _editZoneName( clientId, self ), lambda clientId: self.zoneTemplate.name )
            ]

        self.form = Form( menuItems, lambda clientId, abort=False: finishCallback( clientId, session, abort ) )
        self.form.prompt = endl + "{!{FB<select an option>"

    def activate( self, clientId ):
        self.form.activate( clientId )

def _editZoneNameCallback( clientId, zoneTemplateForm, zoneName ):
    zoneTemplateForm.zoneTemplate.name = zoneName
    popPrompt( clientId )
    sendToClient( clientId, zoneTemplateForm.form.menu( clientId ) )

def _editZoneName( clientId, zoneTemplateForm ):
    getOneLine( clientId, lambda clientId, text: _editZoneNameCallback( clientId, zoneTemplateForm, text ) )
    pushPrompt( clientId, lambda clientId: endl + "{!{FU<input new name for {FY%s{FU>" % zoneTemplateForm.zoneTemplate.name )

    
    
