__author__ = 'olesya'

import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from engine.result_parser import ResultParser
from engine.languages_API import LanguagesAPI


class JavaTest(unittest.TestCase):
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

    def test_find_by_id_get_for_statement_python(self):
        """
        Test getting translation for "for statement" in python from html by given id
        """
        a = LanguagesAPI()
        result, code = a.http_request_using_urlfetch("https://docs.python.org/2/reference/compound_stmts.html#the-for-statement", {})
        b = ResultParser("Python")
        res = b.find_by_id(result, 'the-for-statement')
        self.assertNotEqual(res, "", "The result is empty string!")

    def test__find_by_p_get_for_statement_c(self):
        """
        Test getting translation for "for statement" in c from html by given p
        """
        a = LanguagesAPI()
        cntb = "for"  # code needed to be translated
        result, code = a.http_request_using_urlfetch("http://www.tutorialspoint.com/cprogramming/c_for_loop.htm", {})
        b = ResultParser("c")
        res = b.find_by_p(result)
        print res
        self.assertTrue(cntb in res)

    def test_strip_text_from_html__for_statement_python(self):
        a = LanguagesAPI()
        result, code = a.http_request_using_urlfetch("https://docs.python.org/2/reference/compound_stmts.html#the-for-statement", {})
        b = ResultParser("Python")
        res = b.strip_text_from_html(result)
        self.assertNotIn("<", res, "The result contains tags!")

    def tearDown(self):
        self.testbed.deactivate()