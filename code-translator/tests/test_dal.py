__author__ = 'olesya'

import unittest
from DAL import *
from models.models import *
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class DALTest(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub(Users)
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()
        self.mydb = DAL()

    def test_add_user_check_user_added_by_getting_role(self):
        """
        Test saving user in DB and getting his level after
        """
        DAL.add_new_user("Olesya", "Shapira", "Oles_ka", "123", "olesya@list.ru", "admin")
        role = self.mydb.get_user_level("olesya@list.ru")
        print role
        self.assertEqual(role, 'admin')

    def test_check_unique_user_exception_thrown_if_user_already_exist(self):
        """
        Test to check unique user saved in DB by email
        """
        DAL.add_new_user("Olesya", "Shapira", "Oles_ka", "123", "olesya@list.ru", "admin")
        self.assertRaises(UserExistException, DAL.add_new_user, "Olesya", "Shapira", "Oles_ka", "123",
                          "olesya@list.ru", "admin")

    def test_add_new_data(self):
        """
        Test saving data in DB and getting data from DB
        """
        DAL.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=True)
        data = DAL.get_data_from_db("for", "java")
        print data
        self.assertIsNotNone(data)

    def test_check_unique_keyword_exception_thrown_if_keyword_already_exist(self):
        """
        Test to check unique data saved in DB for each keyword
        """
        DAL.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=True)
        self.assertRaises(DataExistException, DAL.save_data_in_db, "java", "for", "statement", "https://docs....",
                          "the for statement is ...", True)

    def tearDown(self):
        self.testbed.deactivate()