__author__ = 'olesya'

import unittest
from translation_engine.translation_engine import TranslationEngine
from engine.languages_API import LanguagesAPI
from google.appengine.ext import testbed
from DAL import *
from translation_engine.my_parser import *

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
        url = self.t.url_search("for", "keyword")
        self.assertEqual("https://docs.oracle.com/javase/tutorial/java/nutsandbolts/for.html", url)

    def test_google_search_while_python_get_default_url(self):
        """
        Test google search for language = python, make sure url is from the chosen site
        """
        self.l = "Python"
        self.t = TranslationEngine(self.l)
        url = self.t.url_search("while", "keyword")
        self.assertIn("http://www.tutorialspoint.com/python/python_while_loop.htm", url)

    def test_google_search_if_python_get_default_url(self):
        """
        Test google search for language = python, make sure url is from the chosen site
        """
        self.l = "Python"
        self.t = TranslationEngine(self.l)
        url = self.t.url_search("if", "keyword")
        print url
        self.assertIn("https://docs.python.org/3/tutorial/controlflow.html", url)

    def test_google_search_second_page_java_goto(self):
        """
        Test google search for language = java, make sure url is from the chosen site from second page
        """
        self.l = "Java"
        self.t = TranslationEngine(self.l)
        url = self.t.url_search("goto", "keyword")
        print url
        self.assertIn("http://docs.oracle.com/javase/tutorial/java/nutsandbolts/_keywords.html", url)

    def test_add_keyword_python_return(self):
        """
        Test add keyword for language = python, make sure the data is saved in db
        """
        self.l = "Python"
        self.t = TranslationEngine(self.l)
        self.t.add_keyword("return", "keyword")
        data = None
        try:
            data = DAL.get_data_from_db("return", "Python")
            print 20*"-"
            print data
        except DataNotExistException:
            print "error"
        expected = '<div class="section" id="simple-statements">'
        self.assertEqual(expected, data["translation"].split('\n')[0])

    def test_add_keyword_java(self):
        """
        Test add keyword for language = java, make sure the data is saved in db
        """
        self.l = "Java"
        self.t = TranslationEngine(self.l)
        self.t.add_keyword("while", "keyword")
        data = None
        try:
            data = DAL.get_data_from_db("while", "Java")
            print 20*"-"
            print data
        except DataNotExistException:
            print "error"
        expected = '<div id="PageContent">'
        self.assertEqual(expected, data["translation"].split('\n')[0])

    def test_add_keyword_ruby(self):
        """
        Test add keyword for language = ruby, make sure the data is saved in db
        """
        self.l = "Ruby"
        self.t = TranslationEngine(self.l)
        self.t.add_keyword("for", "keyword")
        data = None
        try:
            data = DAL.get_data_from_db("for", "Ruby")
            print 20*"-"
            print data
        except DataNotExistException:
            print "error"
        expected = '<div class="col-md-7 middle-col">'
        self.assertTrue(expected, data['translation'].split('\n')[0])

    def test_get_translation_java_code(self):
        """
        Test all way from giving code text to getting response
        Given 3 keywords, expected list of 3 translations
        """
        self.l = "Java"
        self.t = TranslationEngine(self.l)
        code_text = "for while if"
        transaltion_list, final_code_text = self.t.get_translation(code_text)
        print(transaltion_list)
        self.assertEqual(len(transaltion_list), 3)

    def test_parse_result_python_for(self):
        self.l = "Python"
        self.t = TranslationEngine(self.l)
        url = self.t.url_search("for", "keyword")
        la = LanguagesAPI()
        result, code = la.http_request_using_urlfetch(http_url=url)
        res = self.t.parse_result(result)
        self.assertEqual(res.split('\n')[0], '<div class="col-md-7 middle-col">')

    def test_get_translation_python_comment(self):
        """
        """
        self.l = "Python"
        self.t = TranslationEngine(self.l)
        code_text = "#comment"
        transaltion_list, final_code_text = self.t.get_translation(code_text)
        print(final_code_text)
        expected = '<span class="comment">#</span><span class="comment">comment</span>'
        self.assertEqual(final_code_text, expected)

    def test_add_tag(self):
        self.l = "Python"
        self.t = TranslationEngine(self.l)
        expected = '<span class="keyword">if</span>'
        res = self.t.add_tag("keyword", "if")
        self.assertEqual(expected, res)

    def test_reformat_parsed_text_keywords(self):
        self.l = "Python"
        self.parser_obj = Parser(self.l)
        self.t = TranslationEngine(self.l)
        code_text = "for if \n  while"
        print code_text
        transaltion_list, parsed = self.parser_obj.run_parser(code_text)
        expected = '<span class="keyword">for</span> <span class="keyword">if</span> \n  ' \
                   '<span class="keyword">while</span>'
        res = self.t.reformat_parsed_text(code_text, parsed)
        self.assertEqual(expected, res)

    def test_reformat_parsed_text_keywords_and_words(self):
        self.l = "Python"
        self.parser_obj = Parser(self.l)
        self.t = TranslationEngine(self.l)
        code_text = "for(i) if \n  while"
        print code_text
        transaltion_list, parsed = self.parser_obj.run_parser(code_text)
        expected = '<span class="keyword">for</span>(i) <span class="keyword">if</span> \n  ' \
                   '<span class="keyword">while</span>'
        res = self.t.reformat_parsed_text(code_text, parsed)
        self.assertEqual(expected, res)

    def test_reformat_parsed_text_comments(self):
        self.l = "Python"
        self.parser_obj = Parser(self.l)
        self.t = TranslationEngine(self.l)
        code_text = "#comment"
        print code_text
        transaltion_list, parsed = self.parser_obj.run_parser(code_text)
        expected = '<span class="comment">#</span><span class="comment">comment</span>'
        res = self.t.reformat_parsed_text(code_text, parsed)
        self.assertEqual(expected, res)

    def test_reformat_parsed_text_functions(self):
        self.l = "Python"
        self.parser_obj = Parser(self.l)
        self.t = TranslationEngine(self.l)
        code_text = "foo()"
        print code_text
        transaltion_list, parsed = self.parser_obj.run_parser(code_text)
        expected = '<span class="function">foo</span>()'
        res = self.t.reformat_parsed_text(code_text, parsed)
        self.assertEqual(expected, res)

    def test_reformat_parsed_text_strings(self):
        self.l = "Python"
        self.parser_obj = Parser(self.l)
        self.t = TranslationEngine(self.l)
        code_text = '"is a string for test"'
        print code_text
        transaltion_list, parsed = self.parser_obj.run_parser(code_text)
        expected = '"<span class="string">is a string for test</span>"'
        res = self.t.reformat_parsed_text(code_text, parsed)
        self.assertEqual(expected, res)