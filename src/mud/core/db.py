from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from util import isString, isDefined

class DBMetaData:
    def __init__(self):
        self.prefix = ""
        self.types = {}

    def setPrefix( self, prefix ):
        """
        sets the prefix on all dbms database names, e.g. 'BETA'
        
        prefix: string
        """
        assert isString( prefix )
        self.prefix = prefix

    def setType( self, typeName, typeValue ):
        """
        maps a database type, e.g. 'WORLD', to a database type value, e.g 'LAZARUS'
        
        typeName : string
        typeValue: string
            
        this map is injective, i.e. values are distinct
        """
        assert isString( typeName )
        assert isString( typeValue )
            
        assert typeName not in self.types
        for t in self.types:
            assert self.types[ t ] != typeValue
            
        self.types[ typeName ] = typeValue

data = DBMetaData()

def getSession( dbName, dbType, declarativeBase, metadata=data ):
    """
    returns a threadsafe sqlalchemy session, used to access an underlying data model, as described by declarativeBase
    e.g. session.commit(), session.add(user)

    dbName         : string, the logical database name, e.g. 'MOB_DESCRIPTIONS'
    dbType         : string, the persistence type class, e.g. 'STATIC', 'INSTANCE'
    declarativeBase: an instance of sqlalchemy.ext.declarative.declarative_base
    """
    assert isString( dbName )
    assert isString( dbType )
    assert isDefined( declarativeBase )

    assert dbType in metadata.types
    
    dbActualName = "%s_%s_%s" % (metadata.prefix, dbName, metadata.types[ dbType ])

    engine = create_engine('mysql://muduser:mudpass@localhost/%s' % dbActualName )
    declarativeBase.metadata.create_all(engine) 
    
    return scoped_session(sessionmaker(bind=engine))
