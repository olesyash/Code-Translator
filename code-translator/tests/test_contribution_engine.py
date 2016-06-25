__author__ = 'olesya'

import unittest
from contribution_engine.contribution_engine import *
from models.models import *
from google.appengine.ext import ndb
from google.appengine.ext import testbed

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


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
        """
        Test function 'check_keyword_approved'
        Save in DB approved keyword
        Use the function to check if approved, expect true
        """
        res = self.mydb.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=True)
        self.assertTrue(self.ce.check_keyword_approved(res))

    def test_check_keyword_approved_false(self):
        """
        Test function 'check_keyword_approved'
        Save in DB not approved keyword
        Use the function to check if approved, expect false
        """
        res = self.mydb.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=False)
        self.assertFalse(self.ce.check_keyword_approved(res))

    def test_contribute_approved_true(self):
        """
        Test function 'contribute'
        Save in DB  approved keyword
        Use the function to contribute, expect message that keyword already translated
        """
        self.mydb.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=True)
        res = self.ce.contribute()
        self.assertEqual(res, "Thank you, but the keyword already translated")

    def test_contribute_approved_false(self):
        """
        Test function 'contribute'
        Save in DB not approved keyword
        Use the function to contribute, expect the existing translation
        """
        self.mydb.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=False)
        res = self.ce.contribute()
        self.assertEqual(res, "the for statement is ...")

    def test_contribute_not_in_db(self):
        """
        Test function 'contribute'
        Expect request for translation
        """
        self.ce = ContributionEngine("java", "fac")
        res = self.ce.contribute()
        self.assertEqual(res, "Please insert contribution details: ")

    def test_user_approve_true(self):
        """
        Test function 'save_data_in_db'
        Save the translation, get the translation from DB,  expect approved = true
        """
        self.mydb.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=False)
        res = self.ce.user_approve()
        self.assertEqual(res, "Thank you for the keyword approve!")
        data = self.mydb.get_data_from_db("for", "java")
        self.assertTrue(data['approved'])

    def test_get_translation_by_id_wrong_url(self):
        """
        Test function 'get_translation'
        Put wrong url, expect error message "wrong url"
        """
        url = "https://docs.pyth"
        _id = 'the-for-statement'
        res, rc = self.ce.get_translation(url, "id", _id)
        self.assertEqual(res, "We could not use this URL. Please recheck spelling")

    def test_get_translation_by_id_wrong_translation(self):
        """
        Test function 'get_translation'
        Get wrong translation by id, expect error message "wrong translation"
        """
        url = "https://github.com/olesyash/Code-Translator/issues/21"
        _id = 'start-of-content'
        self.ce = ContributionEngine("python", "yield")
        res, rc = self.ce.get_translation(url, "id", _id)
        self.assertEqual(res, "Are you sure this link describing the keyword?")

    def test_get_translation_by_id(self):
        """
        Test function 'get_translation'
        Get translation by id, expect rc = o
        """
        url = "https://docs.python.org/2/reference/compound_stmts.html#the-for-statement"
        _id = 'the-for-statement'
        res, rc = self.ce.get_translation(url, "id", _id)
        self.assertEqual(rc, 0)

    def test_get_translation_by_class(self):
        """
        Test function 'get_translation'
        Get translation by class, expect rc = o
        """
        url = "https://docs.python.org/2/reference/compound_stmts.html#the-for-statement"
        name = 'section'
        res, rc = self.ce.get_translation(url, "class", name)
        self.assertEqual(rc, 0)

    def test_get_translation_by_p_get_wrong_translation(self):
        """
        Test function 'get_translation'
        Get wrong translation by p, expect error message "wrong translation"
        """
        url = "https://docs.python.org/2/reference/compound_stmts.html#the-for-statement"
        res, rc = self.ce.get_translation(url, "p")
        self.assertEqual(res, "Are you sure this link describing the keyword?")

    def test_get_translation_clear(self):
        """
        Test function 'get_translation'
        Get translation as plain text, expect rc = o
        """
        url = "https://docs.python.org/2/reference/compound_stmts.html#the-for-statement"
        res, rc = self.ce.get_translation(url, "clear")
        self.assertEqual(rc, 0)

    def test_get_translation_nothing(self):
        """
        Test function 'get_translation'
        Get translation as html text, expect rc = o
        """
        url = "https://docs.python.org/2/reference/compound_stmts.html#the-for-statement"
        res, rc = self.ce.get_translation(url, "nothing")
        self.assertEqual(rc, 0)

    def test_check_one_entry_on_update_keyword(self):
        """
        Test to check unique data saved in DB for each keyword
        """
        DAL.save_data_in_db("java", "for", "statement", "https://docs....", "the for statement is ...", approved=False)
        self.ce.save_in_db("keyword", "link2", "the for statement is ...")
        _qry = LanguagesData.query(LanguagesData.language == "java", LanguagesData.keyword == "for")
        self.assertEqual(_qry.count(), 1)

    def test_check_if_keyword_ok(self):
        """
        Test check_is_keyword
        Save keyword, make sure function return True
        :return: boolean
        """
        self.ce = ContributionEngine("Java", "for")
        res = self.ce.check_is_keyword()
        self.assertTrue(res)

    def test_check_if_keyword_wrong(self):
        """
        Test check_is_keyword
        Save non keyword, make sure function return True
        :return: boolean
        """
        self.ce = ContributionEngine("Java", "fo")
        res = self.ce.check_is_keyword()
        self.assertFalse(res)

    def tearDown(self):
        self.testbed.deactivate()