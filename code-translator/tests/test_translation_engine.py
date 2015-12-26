__author__ = 'olesya'

import unittest
from translation_engine.translation_engine import TranslationEngine
from translation_engine.languages_specific_features import *
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from DAL import *


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
        self.l = "java"
        self.t = TranslationEngine(self.l)

    def test_google_search_for_java_get_default_url(self):
        url = self.t.google_search("for")
        self.assertIn(default_urls[self.l], url)

    def test_google_search_while_python_get_default_url(self):
        self.l = "python"
        self.t = TranslationEngine(self.l)
        url = self.t.google_search("while")
        self.assertIn(default_urls[self.l], url)

    def test_add_keyword_python(self):
        self.l = "python"
        self.t = TranslationEngine(self.l)
        self.t.add_keyword("while", "statement")
        try:
            data = DAL.get_data_from_db("while", "python")
            print 20*"-"
            print data
            self.assertIsNotNone(data)
        except DataNotExistException:
            print "error"

    def test_add_keyword_java(self):
        self.l = "java"
        self.t = TranslationEngine(self.l)
        self.t.add_keyword("while", "statement")
        try:
            data = DAL.get_data_from_db("while", "java")
            print 20*"-"
            print data
            self.assertIsNotNone(data)
        except DataNotExistException:
            print "error"