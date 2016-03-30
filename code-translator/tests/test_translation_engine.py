__author__ = 'olesya'

import unittest
from translation_engine.translation_engine import TranslationEngine
from translation_engine.languages_specific_features import *
from google.appengine.ext import testbed
from DAL import *

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class TranslationEngineTest(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()
        self.testbed.init_urlfetch_stub()

    def test_google_search_for_java_get_default_url(self):
        """
        Test google search for language = java, make sure url is from the chosen site
        """
        self.l = "Java"
        self.t = TranslationEngine(self.l)
        url = self.t.google_search("for", "statement")
        self.assertIn(default_urls[self.l], url)

    def test_google_search_while_python_get_default_url(self):
        """
        Test google search for language = python, make sure url is from the chosen site
        """
        self.l = "Python"
        self.t = TranslationEngine(self.l)
        url = self.t.google_search("while", "statement")
        self.assertIn(default_urls[self.l], url)

    def test_google_search_if_python_get_default_url(self):
        """
        Test google search for language = python, make sure url is from the chosen site
        """
        self.l = "Python"
        self.t = TranslationEngine(self.l)
        url = self.t.google_search("if", "statement")
        print url
        self.assertIn(default_urls[self.l], url)

    def test_add_keyword_python(self):
        """
        Test add keyword for language = python, make sure the data is saved in db
        """
        self.l = "Python"
        self.t = TranslationEngine(self.l)
        self.t.add_keyword("while", "statement")
        data = None
        try:
            data = DAL.get_data_from_db("while", "Python")
            print 20*"-"
            print data
        except DataNotExistException:
            print "error"
        self.assertIsNotNone(data)

    def test_add_keyword_java(self):
        """
        Test add keyword for language = java, make sure the data is saved in db
        """
        self.l = "Java"
        self.t = TranslationEngine(self.l)
        self.t.add_keyword("while", "statement")
        data = None
        try:
            data = DAL.get_data_from_db("while", "Java")
            print 20*"-"
            print data
        except DataNotExistException:
            print "error"
        self.assertIsNotNone(data)

    def test_get_translation_java_code(self):
        """
        Test all way from giving code text to getting response
        Given 3 keywords, expected list of 3 translations
        """
        self.l = "Java"
        self.t = TranslationEngine(self.l)
        code_text = "for while if"
        transaltion_list = self.t.get_translation(code_text)
        print(transaltion_list)
        self.assertEqual(len(transaltion_list), 3)