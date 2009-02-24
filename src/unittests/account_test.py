import unittest
import account

class AccountTest(unittest.TestCase):

    def setUp(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        self.engine = create_engine('sqlite:///:memory:')
        self.Session = sessionmaker(bind=self.engine)
        self.ses = self.Session()
        account.Account.metadata.create_all(self.engine)
    
    def testaccount_name_doesnt_exist(self):
        account.session = self.ses
        self.assert_( account.nameUnused( "Jim" ) )

    def testaccount_name_does_exist(self):
        account.session = self.ses
        account.add(account.Account("spiritic", "123" ))
        self.assert_( not account.nameUnused( "spiritic" ) )
    
    def testget_account_doesnt_exist(self):
        account.session = self.ses
        self.assert_( not account.get("spiritic") )

    def testget_account_exists(self):
        account.session = self.ses
        account.add(account.Account("spiritic", "123" ))
        self.assert_( account.get("spiritic") )
        




        
