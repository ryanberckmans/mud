from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from util import isString, isDefined

dbPrefix = ""
dbTypes = {}
dbEngines = {}

def setPrefix( prefix ):
    isString( prefix )

    dbPrefix = prefix    

def setType( typeName, typeValue ):
    isString( typeName )
    isString( typeValue )

    assert typeName not in dbTypes
    
    dbTypes[ typeName ] = typeValue

def getSession( dbName, dbType, declarativeBase ):
    isString( dbName )
    isString( dbType )
    isDefined( declarativeBase )

    assert dbType in dbTypes
    
    dbActualName = "%s_%s_%s" % (dbPrefix, dbName, dbTypes[ dbType ])
    engine = None

    if (dbActualName in dbEngines ):
        raise EngineAlreadyExists()
    else:
        dbEngines[ dbActualName ] = create_engine('mysql://muduser:mudpass@localhost/%s' % dbActualName )
        engine = dbEngines[ dbActualName ]
        metadata.create_all(engine) 
    
    metadata.create_all(engine) 

    return scoped_session(sessionmaker(bind=engine))



class EngineAlreadyExists(Exception):
    def __init__(self):
        pass

    
