__author__ = 'olesya'

import unittest
import logging
from models.models import *
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from translation_engine.parser import *
from translation_engine.translation_engine import TranslationEngine
from contribution_engine.contribution_engine import ContributionEngine

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
import json


class AddNewLanguageTest(unittest.TestCase):
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

    def test_prepare_for_lexicon_python_keywords(self):
        """
        Test prepare for lexicon function, for existing in code language - Python
        """
        dl = LanguagesSpecificFeatures("Python")
        res = dl.prepare_for_lexicon("keywords")
        self.assertIsInstance(res, Alt)

    def test_get_prepare_for_lexicon_C_empty(self):
        """
        Test prepare for lexicon function, for new language - C,  with empty DB
        """
        dl = LanguagesSpecificFeatures("C")
        res = dl.prepare_for_lexicon("keywords")
        self.assertIsInstance(res, Alt)

    def test_prepare_for_lexicon_C_not_empty(self):
        """
        Test prepare for lexicon function, for new language - C,  after saving in DB
        """
        stmtns = ["for", "if", "else"]
        dl = LanguagesSpecificFeatures("C")
        data = {"statements": stmtns}
        dal = DAL()
        dal.save_language_data("C", data)
        res = dl.prepare_for_lexicon("keywords")
        self.assertIsInstance(res, Alt)

    def test_cllasify_c(self):
        """
        Test classification after saving in DB for new language C
        """
        tr = TranslationEngine("C")
        ndb.get_context().clear_cache()
        stmtns = ["for", "if", "else"]
        DAL.save_classification("C", "statement", stmtns)
        res = tr.classify_keywords("for", "keyword")
        self.assertEqual(STATEMENT, res)

    def test_keyword_in_other(self):
        """
        Test keyword_in_other function, after saving in DB DB for new language C
        """
        definition = ["ifdef"]
        DAL.save_classification("C", "example", ["stam"])
        DAL.save_classification("C", "definition", definition)
        res = get_keyword_classification("C", "ifdef")
        self.assertEqual(res, "definition")

    def test_classify_keyword_in_other(self):
        """
        Test classification in others, after saving in DB for new language C
        """
        definition = ["ifdef"]
        tr = TranslationEngine("C")
        DAL.save_classification("C", "example", ["stam"])
        DAL.save_classification("C", "definition", definition)
        res = tr.classify_keywords("ifdef", "keyword")
        self.assertEqual(res, "definition")

    def test_add_new_language_json_C_check_real_code(self):
        """
        Test add new language function, add new language c and run parser on it
        """
        ndb.get_context().clear_cache()
        data = dict()
        ce = ContributionEngine("C")
        data['keywords'] = ["auto", "else", "long", "switch", "break", "enum", "register", "typedef", "case", "extern",
                            "char", "float", "short", "unsigned", "const", "for", "signed", "continue", "goto", 'void',
                            "volatile", "default", "if", "static", "while", "do", "int", "struct", "_Packed", "double",
                            "return", "union",  "sizeof"]
        data['str_symbol1'] = [str_symbol1]
        data['str_symbol2'] = [str_symbol2]
        data['operations'] = ['+', '-', '*', '/', '%', '++', '--',  '==', '!=', '<', '<=', '>', '>=', '=', '&', '|', '^',
                              '<<', '>>', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=', '<<=', '>>=', '&=', '^=',
                              '?', ':', '~', '|=']
        data['add_library'] = ["include"]
        data['literals'] = []
        data['start_comment_symb'] = ['//']
        data['comment_start1'] = ['/*']
        data['comment_end1'] = ['*/']
        data['comment_start2'] = []
        data['comment_end2'] = []
        data['func_def'] = []
        data['class_keyword'] = []
        data['escape_character'] = ['\\']
        data['func_start'] = ['(']
        data['function_call_char'] = ['(']
        data['function_call_must_char'] = "True"
        data['other'] = {}
        json_data = json.dumps(data)
        ce.add_new_language_json(json_data)
        dal = DAL()
        res = dal.get_all_data_for_language("C")
        print res
        self.filename = "parser_tests/c_real_code.txt"
        self.run_parser()

        expected_lib = ['HashTable.h']
        expected_keywords = ['include', 'void', 'int', 'char', 'if', 'return', 'for']
        expected_functions_calls = ['freeTable', 'freeList', 'free', 'free']
        self.assertEqual(expected_keywords, self.p.keywords)
        self.assertEqual(expected_functions_calls, self.p.scanner.functions_calls)
        self.assertEqual(expected_lib, self.p.scanner.libraries)


    def run_parser(self):
        """
        This internal function is used in all tests to read tokens using parser
        """
        f = open(self.filename, "r")
        output = f.read()
        self.p = Parser("C")
        self.p.run_parser(output)

    def test_get_all_urls_for_python(self):
        """
        Test get_all_urls function, for existing in code language - python
        """
        expected = ["https://docs.python.org/", "https://wiki.python.org", "http://www.tutorialspoint.com/python"]
        res = get_urls_for_language("Python")
        self.assertEqual(expected, res)

    def test_get_urls_for_c_empty(self):
        """
        Test get_all_urls function, for new language - c, when the DB is empty
        """
        res = get_urls_for_language("C")
        self.assertEqual(res, [])

    def test_save_and_retrieve_all_urls_for_c(self):
        """
        Test get_all_urls function, for new language - c, after adding it to DB
        """
        data = {"urls": ["c_url1", "c_url2"], "c_url1": {"type": "class", "name": "section"},
                                              "c_url2": {"type": "id", "name": "content"}}
        ce = ContributionEngine("C", "")
        ce.add_urls_for_language(data)
        res = get_urls_for_language("C")
        self.assertEqual(data["urls"], res)

    def test_save_and_retrieve_all_details_for_url_c(self):
        """
        Test get all details about url, after saving it in DB using 'add_urls_for_language' function
        """
        data = {"urls": ["c_url1", "c_url2"], "c_url1": {"type": "class", "name": "section"},
                                              "c_url2": {"type": "id", "name": "content"}}
        ce = ContributionEngine("C", "")
        ce.add_urls_for_language(data)
        _type, name = get_details_about_url("c_url1")
        self.assertEqual(_type, "class")
        self.assertEqual(name, "section")
        _type, name = get_details_about_url("c_url2")
        self.assertEqual(_type, "id")
        self.assertEqual(name, "content")
        _type, name = get_details_about_url("https://wiki.python.org")
        self.assertEqual(_type, "id")
        self.assertEqual(name, "content")

    def test_add_classification_for_language_classify(self):
        """
        Test add_classification_for_language function, use classify function to test
        """
        ndb.get_context().clear_cache()
        data = {"statements": ["for", "if", "else"], "operators": ['signed'], "data_types": ["int", "long", "float", "char",
                "double"], "expressions": ['sizeof'], "other": []}
        tr = TranslationEngine("C")
        ce = ContributionEngine("C")
        ce.add_classification_for_language(data)
        self.assertEqual("statement", tr.classify_keywords("for", "keyword"))
        self.assertEqual("data type", tr.classify_keywords("int", "keyword"))
        self.assertEqual("expression", tr.classify_keywords("sizeof", "keyword"))
        self.assertEqual("operator", tr.classify_keywords("signed", "keyword"))

    def tearDown(self):
        self.testbed.deactivate()

