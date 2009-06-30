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
        
    def test_getSessionParamsNotString(self):
        asserts( self, db.getSession, 3, None, None )
        asserts( self, db.getSession, "", 3, None )

    def test_getSessionBaseNone(self):
        asserts( self, db.getSession, "", "", None )

    def test_getSessionTwice(self):
        isDefined( db.getSession("TEST", "test-type", self.base, db.data ) )
        isDefined( db.getSession("TEST", "test-type", self.base, db.data ) )

    def test_getSessionTwoDBsSameType(self):
        isDefined( db.getSession("TEST", "test-type", self.base, db.data ) )
        isDefined( db.getSession("TEST2", "test-type", self.base, db.data ) )

    def test_getSessionTwoDBsDifferentType(self):
        isDefined( db.getSession("TEST", "test-type", self.base, db.data ) )
        isDefined( db.getSession("TEST2", "test-type2", self.base, db.data ) )

#    def test_findDefaultCallbackFromEpsilon(self):
#        self.assert_( call(self.map.find("")) == "default" )
#        self.assertRaises(AssertionError, self.map.addCmd, None, f("a"))
