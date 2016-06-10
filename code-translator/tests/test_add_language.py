__author__ = 'olesya'

import unittest
import logging
from models.models import *
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from translation_engine.my_parser import *
from translation_engine.translation_engine import TranslationEngine
from contribution_engine.contribution_engine import ContributionEngine

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


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
        res = prepare_for_lexicon("Python", "keywords")
        self.assertEqual(python_keywords, res)

    def test_get_prepare_for_lexicon_C_empty(self):
        res = prepare_for_lexicon("C", "keywords")
        self.assertIsInstance(res, Alt)

    def test_prepare_for_lexicon_C_not_empty(self):
        stmtns = ["for", "if", "else"]
        DAL.save_language_details("C", "keywords", stmtns)
        res = prepare_for_lexicon("C", "keywords")
        self.assertIsInstance(res, Alt)

    def test_cllasify_c(self):
        tr = TranslationEngine("C")
        ndb.get_context().clear_cache()
        stmtns = ["for", "if", "else"]
        DAL.save_language_details("C", "statements", stmtns)
        res = tr.classify_keywords("for", "keyword")
        self.assertEqual(STATEMENT, res)

    def test_keyword_in_other(self):
        definition = ["ifdef"]
        DAL.save_language_details("C", "example", ["stam"])
        DAL.save_language_details("C", "definition", definition)
        res = keyword_in_other("C", "ifdef")
        self.assertEqual(res, "definition")

    def test_callsify_keyword_in_other(self):
        definition = ["ifdef"]
        tr = TranslationEngine("C")
        DAL.save_language_details("C", "example", ["stam"])
        DAL.save_language_details("C", "definition", definition)
        res = tr.classify_keywords("ifdef", "keyword")
        self.assertEqual(res, "definition")

    def test_add_new_language_C_check_real_code(self):
        ndb.get_context().clear_cache()
        data = dict()
        ce = ContributionEngine("C", "")
        data['keywords'] = ["auto", "else", "long", "switch", "break", "enum", "register", "typedef", "case",	"extern",
                            "char", "float", "short", "unsigned", "const", "for", "signed", "continue", "goto", 'void',
                            "volatile", "default", "if", "static", "while", "do", "int", "struct", "_Packed", "double",
                            "return", "union",  "sizeof"]

        data['str_symbol1'] = ["'"]
        data['str_symbol2'] = ['"']
        data['operations'] = ['+', '-', '*', '/', '%', '++', '--',  '==', '!=', '<', '<=', '>', '>=', '=', '&', '|', '^',
                              '<<', '>>', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=', '<<=', '>>=', '&=', '^=',
                              '?', ':', '~', '|=']

        data['add_library'] = ["include"]
        data['literals'] = []
        data['start_comment_symb'] = ['//']
        data['comment_start1'] = ['/*']
        data['comment_start2'] = ['*/']
        data['func_def'] = []
        data['class_keyword'] = []
        data['escape_character'] = []
        data['func_start'] = []
        data['function_call_char'] = ['(']
        data['function_call_must_char'] = ["True"]
        data['other'] = {}

        ce.add_new_language(data)
        self.filename = "parser_tests/c_real_code.txt"
        self.run_parser()

        expected_lib = ['HashTable.h']
        expected_keywords = ['include', 'void', 'int', 'if', 'return', 'for']
        expected_functions_calls = ['freeTable', 'freeList', 'free', 'free']
        # self.assertEqual(expected_keywords, self.p.keywords)
        # self.assertEqual(expected_functions_calls, self.p.scanner.functions_calls)
        self.assertEqual(expected_lib, self.p.scanner.libraries)

    def run_parser(self):
        """
        This internal function is used in all tests to read tokens using parser
        """
        f = open(self.filename, "r")
        output = f.read()
        self.p = Parser("C")
        self.p.run_parser(output)


