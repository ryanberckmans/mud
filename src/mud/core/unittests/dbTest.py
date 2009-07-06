import unittest
from test import asserts
from util import isDefined
from .. import db

class TestDBPrefix(unittest.TestCase):

    def setUp(self):
        db.data = db.DBMetaData()

    def test_prefixNotString(self):
        asserts( self, db.data.setPrefix, None)
        asserts( self, db.data.setPrefix, 12)

    def test_prefix(self):
        db.data.setPrefix( "abc" )
        self.assert_( db.data.prefix == "abc" )

class TestDBTypes(unittest.TestCase):

    def setUp(self):
        db.data = db.DBMetaData()

    def test_typeNotString(self):
        asserts( self, db.data.setType, None, None )
        asserts( self, db.data.setType, 12, None )
        asserts( self, db.data.setType, "", None )
        asserts( self, db.data.setType, 7, "" )

    def test_typeEmptyString(self):
        db.data.setType( "", "" )
        self.assert_( db.data.types[""] == "" )

    def test_typeDuplicate(self):
        db.data.setType( "abc", "" )
        asserts( self, db.data.setType, "abc", "jim" )

    def test_typeDistinctValues(self):
        db.data.setType( "abc", "def" )
        asserts( self, db.data.setType, "def", "def" )

class TestDBGetSession(unittest.TestCase):
    def setUp(self):
        db.data = db.DBMetaData()
        db.data.setType( "test-type", "WORLD" )
        db.data.setType( "test-type2", "STATIC" )
        db.data.setPrefix("BETA")
        from sqlalchemy.ext.declarative import declarative_base
        self.base = declarative_base()
        
    def test_getSessionFactoryParamsNotString(self):
        asserts( self, db.getSessionFactory, 3, None, None )
        asserts( self, db.getSessionFactory, "", 3, None )

    def test_getSessionFactoryBaseNone(self):
        asserts( self, db.getSessionFactory, "", "", None )

    def test_getSessionFactoryTwice(self):
        assert isDefined( db.getSessionFactory("TEST", "test-type", self.base, db.data ) )
        assert isDefined( db.getSessionFactory("TEST", "test-type", self.base, db.data ) )

    def test_getSessionFactoryTwoDBsSameType(self):
        assert isDefined( db.getSessionFactory("TEST", "test-type", self.base, db.data ) )
        assert isDefined( db.getSessionFactory("TEST2", "test-type", self.base, db.data ) )

    def test_getSessionFactoryTwoDBsDifferentType(self):
        assert isDefined( db.getSessionFactory("TEST", "test-type", self.base, db.data ) )
        assert isDefined( db.getSessionFactory("TEST2", "test-type2", self.base, db.data ) )

#    def test_findDefaultCallbackFromEpsilon(self):
#        self.assert_( call(self.map.find("")) == "default" )
#        self.assertRaises(AssertionError, self.map.addCmd, None, f("a"))
