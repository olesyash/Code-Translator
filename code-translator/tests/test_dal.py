__author__ = 'olesya'

import unittest
from DAL import *
from models.models import *
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from translation_engine.languages_specific_features import *


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

    def test_save_and_read_new_language_c_statements(self):
        """
        Test save in DB details for new language c
        """
        ndb.get_context().clear_cache()
        stmtns = ["for", "if", "else"]
        DAL.save_language_details("C", "statements", stmtns)
        res = DAL.get_language_details("C", "statements")
        self.assertEqual(stmtns, res)

    def test_save_new_language_get_all_languages(self):
        """
        Test save in DB new language and retrieve ist of languages from DB
        """
        dal = DAL()
        ndb.get_context().clear_cache()
        res = dal.add_language("C")
        get = dal.get_all_languages()
        self.assertEqual(True, res)
        self.assertEqual(["C"], get)

    def test_add_few_languages(self):
        dal = DAL()
        dal.add_language(languages)
        res = dal.get_all_languages()
        self.assertEqual(languages, res)

    def test_add_existing_language_get_false(self):
        dal = DAL()
        for l in languages:
            print "dal add language" + str(dal.add_language(l))
            print "dal get all languages" + str(dal.get_all_languages())
        res = dal.add_language(languages[0])
        self.assertFalse(res)

    def tearDown(self):
        self.testbed.deactivate()