__author__ = 'olesya'

import unittest
from contribution_engine.contribution_engine import *
from models.models import *
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class ContributionTest(unittest.TestCase):
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
        self.testbed.init_urlfetch_stub()
        self.mydb = DAL()
        self.ce = ContributionEngine("java", "for")

    def test_check_keyword_approved_true(self):
        res = self.mydb.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=True)
        self.assertTrue(self.ce.check_keyword_approved(res))

    def test_check_keyword_approved_false(self):
        res = self.mydb.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=False)
        self.assertFalse(self.ce.check_keyword_approved(res))

    def test_contribute_approved_true(self):
        self.mydb.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=True)
        res = self.ce.contribute()
        self.assertEqual(res, "Thank you, but the keyword already translated")

    def test_contribute_approved_false(self):
        self.mydb.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=False)
        res = self.ce.contribute()
        self.assertEqual(res, "the for statement is ...")

    def test_contribute_not_in_db(self):
        self.ce = ContributionEngine("java", "fac")
        res = self.ce.contribute()
        self.assertEqual(res, "Please insert contribution details: ")

    def test_user_approve_true(self):
        self.mydb.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=False)
        res = self.ce.user_approve(True)
        self.assertEqual(res, "Thank you for keyword approve")
        data = self.mydb.get_data_from_db("for", "java")
        self.assertTrue(data['approved'])

    def test_get_translation_by_id(self):
        url = "https://docs.python.org/2/reference/compound_stmts.html#the-for-statement"
        _id = 'the-for-statement'
        res = self.ce.get_translation_by_id("keyword", url, _id)
        self.assertEqual(res, "Thank you for your contribution!")

    def test_get_translation_by_id_wrong_url(self):
        url = "https://docs.pyth"
        _id = 'the-for-statement'
        res = self.ce.get_translation_by_id("keyword", url, _id)
        self.assertEqual(res, "We could not use this URL. Please recheck spelling")

    def test_get_translation_by_id_wrong_transaltion(self):
        url = "https://github.com/olesyash/Code-Translator/issues/21"
        _id = 'start-of-content'
        self.ce = ContributionEngine("python", "yield")
        res = self.ce.get_translation_by_id("keyword", url, _id)
        self.assertEqual(res, "Are you sure this link describing the keyword?")






