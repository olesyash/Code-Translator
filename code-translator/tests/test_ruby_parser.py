__author__ = 'olesya'

import unittest
from translation_engine.my_parser import *

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class MyParserRubyTest(unittest.TestCase):
    def test_ruby_keywords(self):
        """
        This test is testing parser for finding all keywords in ruby code
        """
        self.filename = "parser_tests/ruby_keywords.txt"
        self.run_parser()
        expected_keywords = ['def', 'return', 'unless', 'return', 'end']
        self.assertEqual(expected_keywords, self.p.keywords)

    def test_ruby_literals(self):
        """
        This test is testing parser for finding all literals in ruby code
        """
        self.filename = "parser_tests/ruby_literals.txt"
        self.run_parser()
        expected_literals = ['true', 'false', 'nil']
        self.assertEqual(expected_literals, self.p.literals)

    def test_find_all_operations(self):
        """
        This test is testing parser for finding all operations in ruby code
        """
        self.filename = "parser_tests/ruby_operations.txt"
        expected_operations = ['=', '+=', '-=', '*=', '**=', '/=', '==', '>', '>', '~', '~', '-',
                               '&', '&', '^', '^', '|', '|', '<<', '<<', '>>', '>>']
        self.run_parser()
        self.assertListEqual(expected_operations, self.p.operations)

    def test_ignore_one_line_comments(self):
        """
        This test is testing parser for ignore all one line comments
        """
        self.filename = "parser_tests/ruby_comments.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_ignore_two_lines_comments(self):
        """
        This test is testing parser for ignore all two lines comments
        """
        self.filename = "parser_tests/ruby_2_lines_comments.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_ignore_strings(self):
        """
        This test is testing parser for ignore all strings in ruby code
        """
        self.filename = "parser_tests/ruby_strings.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_ruby_require(self):
        """
        This test is testing parser for finding all libraries in ruby code
        """
        self.filename = "parser_tests/ruby_imports.txt"
        self.run_parser()
        expected_keywords = ["require", "require"]
        self.assertEqual(expected_keywords, self.p.keywords)

    def test_ruby_libraries(self):
        """
        This test is testing parser for for finding all keywords of libraries import in ruby code
        """
        self.filename = "parser_tests/ruby_imports.txt"
        self.run_parser()
        expected_libraries = ['support', 'moral']
        self.assertEqual(expected_libraries, self.p.scanner.libraries)

    def test_find_all_func_def(self):
        """
        This test is testing parser for finding all functions declarations in ruby code
        """
        self.filename = "parser_tests/ruby_function_def.txt"
        expected_func_def = ["method_name", "test"]
        self.run_parser()
        self.assertListEqual(expected_func_def, self.p.scanner.functions)

    def test_classes(self):
        """
        This test is testing parser for finding all classes declarations in ruby code
        """
        self.filename = "parser_tests/ruby_classes.txt"
        expected_classes = ["Customer"]
        self.run_parser()
        self.assertListEqual(expected_classes, self.p.scanner.classes)

    def test_find_functions(self):
        """
        This test is testing parser for finding all function calls in ruby code
        """
        self.filename = "parser_tests/ruby_functions.txt"
        expected_functions = ['multiply', 'method_name']
        self.run_parser()
        self.assertListEqual(expected_functions, self.p.scanner.functions_calls)

    def test_ruby_real_code(self):
        """
        This test is testing parser for finding all keywords in real ruby code
        """
        self.filename = "parser_tests/sample.rb"
        self.run_parser()
        expected_keywords = ['require', 'require', 'require', 'require', 'require', 'if', 'end', 'def', 'end']
        expected_lib = ['watir', 'watir\contrib\enabled_popup', 'startClicker', 'net/http', 'net/https']
        expected_func_def = ['setDdlPriority']
        expected_functions_calls = ['contains_text', 'text_field', 'set', 'text_field', 'set', 'button',
                                    'link', 'link', 'select_list', 'select', 'button', 'startClicker',
                                    'setDdlPriority', 'setDdlPriority']
        self.assertEqual(expected_functions_calls, self.p.scanner.functions_calls)
        self.assertEqual(expected_func_def, self.p.scanner.functions)
        self.assertEqual(expected_lib, self.p.scanner.libraries)
        self.assertEqual(expected_keywords, self.p.keywords)

    def run_parser(self):
        """
        This internal function is used in all tests to read tokens using parser
        """
        f = open(self.filename, "r")
        output = f.read()
        self.p = Parser("Ruby")
        self.p.run_parser(output)
