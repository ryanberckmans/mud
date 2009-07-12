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

class MobTemplateForm:

    def __init__( self, mobTemplate, session ):
        assert isDefined( mobTemplate )
        assert isDefined( session )

        assert mobTemplate in session

        self.mobTemplate = mobTemplate
        self.session      = session

        title = endl + "{FYEditing "
        if mobTemplate.id:
            title += "Mob " + str(mobTemplate.id)
        else:
            title += "New Mob"
        
        menuItems = [
            title,
            ( "mob short name", lambda clientId: _editMobShortName( clientId, self ), lambda clientId: self.mobTemplate.sname )
            ]

        self.form = Form( menuItems, lambda clientId, abort=False: finishCallback( clientId, session, abort ) )
        self.form.prompt = endl + "{!{FB<select an option>"

    def activate( self, clientId ):
        self.form.activate( clientId )

def _editMobShortNameCallback( clientId, mobTemplateForm, mobShortName ):
    mobTemplateForm.mobTemplate.sname = mobShortName
    popPrompt( clientId )
    sendToClient( clientId, mobTemplateForm.form.menu( clientId ) )

def _editMobShortName( clientId, mobTemplateForm ):
    getOneLine( clientId, lambda clientId, text: _editMobShortNameCallback( clientId, mobTemplateForm, text ) )
    pushPrompt( clientId, lambda clientId: endl + "{!{FU<input new short name for {FY%s{FU>" % mobTemplateForm.mobTemplate.sname )

    
    
