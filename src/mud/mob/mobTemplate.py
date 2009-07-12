from util import isInt
from sqlalchemy import Column, Integer, String
import mud.core.db as db

def getMobTemplate( templateId ):
    assert isInt( templateId )

    session = getSession()

    mob  = session.query(MobTemplate).filter(MobTemplate.id == templateId ).first()

    session.close()

    return mob

def getSession():
    return _sessionFactory()

class MobTemplate(db.getBase()):
    __tablename__ = 'mob_templates'

    id = Column( Integer, primary_key=True)
    sname = Column( String(64) )
    lname = Column( String(128) )

    def __init__( self ):
        self.sname = "unnamed Mob"
        self.lname = "an unnamed Mob"

    def __str__( self ):
        return "mob template %s, %s" % (self.id, self.sname )

_DB_NAME = "WORLD"
_DB_TYPE = "STATIC"

_sessionFactory = db.getSessionFactory( _DB_NAME, _DB_TYPE )
