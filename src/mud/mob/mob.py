from sqlalchemy import Column, Integer, String, ForeignKey
import mud.core.db as db

def getSession():
    return _sessionFactory()

class Mob(db.getBase()):
    __tablename__ = 'mob_instances'

    id = Column( Integer, primary_key=True)
    templateId = Column( Integer, ForeignKey('mob_templates.id'))
    sname = Column( String(64) )
    lname = Column( String(128) )

    def __init__( self, mobTemplate ):
        _fromTemplate( self, mobTemplate )

    def __str__( self ):
        return "mob instance %s, %s" % (self.id, self.sname )

_DB_NAME = "WORLD"
_DB_TYPE = "STATIC"

_sessionFactory = db.getSessionFactory( _DB_NAME, _DB_TYPE )

def _fromTemplate( mob, mobTemplate ):
    mob.templateId = mobTemplate.id
    mob.sname = mobTemplate.sname
    mob.lname = mobTemplate.lname
