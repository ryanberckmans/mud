from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import mud.core.db as db


def getSession():
    return _sessionFactory()

_Base = declarative_base()

class ZoneTemplate(_Base):
    __tablename__ = 'zone_templates'

    id = Column( Integer, primary_key=True)
    name = Column( String(64) )

    def __init__( self ):
        self.name = "Unnamed Zone"

    def __str__( self ):
        return "zone %s, " % (self.id, self.name )

_DB_NAME = "WORLD"
_DB_TYPE = "STATIC"

_sessionFactory = db.getSessionFactory( _DB_NAME, _DB_TYPE, _Base )
