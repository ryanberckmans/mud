from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
import mud.core.db

Base = declarative_base()

class ZoneTemplate(Base):
    __tablename__ = 'zone_templates'

    id = Column( Integer, primary_key=True)

    def __init__( self ):
        pass

    def __str__( self ):
        return "zone %s" % self.id
