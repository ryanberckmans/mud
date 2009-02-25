from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Account(Base):
    
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False )
    password = Column(String, nullable=False)

    def __init__(self, name, password=None):
        self.name = name.lower()
        self.password = password

    def __repr__(self):
        return "<Account('%s,%s')>" % (self.name, self.password)


engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()
Account.metadata.create_all(engine)


def add( account ):
    assert nameUnused( account.name )
    session.add( account )
    session.commit()


def nameUnused( name ):
    name = name.lower()
    return session.query(Account).filter(Account.name==name).count() == 0


def get( name ):
    name = name.lower()
    try:
        return session.query(Account).filter(Account.name==name).one()
    except NoResultFound:
        return None
    
    
