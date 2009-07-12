from util import isInt
from sqlalchemy import Column, Integer, String
import mud.core.db as db


def getZoneTemplate( templateId ):
    assert isInt( templateId )

    session = getSession()

    zone = session.query(ZoneTemplate).filter(ZoneTemplate.id == templateId ).first()

    session.close()

    return zone

def getSession():
    return _sessionFactory()

class ZoneTemplate(db.getBase()):
    __tablename__ = 'zone_templates'

    id = Column( Integer, primary_key=True)
    name = Column( String(64) )

    def __init__( self ):
        self.name = "Unnamed Zone"

    def __str__( self ):
        return "zone %s, %s" % (self.id, self.name )

_DB_NAME = "WORLD"
_DB_TYPE = "STATIC"

_sessionFactory = db.getSessionFactory( _DB_NAME, _DB_TYPE )
