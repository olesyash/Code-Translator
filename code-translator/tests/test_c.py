__author__ = 'olesya'

import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from engine.result_parser import ResultParser
from engine.languages_API import LanguagesAPI


class CTest(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        #self.testbed.init_datastore_v3_stub(User)
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

        self.testbed.init_urlfetch_stub()

    def test_get_for_statement(self):
        a = LanguagesAPI()
        cntb = "for"  # code needed to be translated
        result, code = a.http_request_using_urlfetch("http://www.tutorialspoint.com/cprogramming/c_for_loop.htm", {})
        b = ResultParser()
        clean_text = b.find_by_p(result)
        print clean_text
        self.assertTrue(cntb in clean_text)