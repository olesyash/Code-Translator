__author__ = 'olesya'

import unittest
from translation_engine.my_parser import *

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class MyParserPythonTest(unittest.TestCase):
    def test_python_keywords(self):
        """
        This test is testing parser for finding all keywords in python code
        """
        self.filename = "parser_tests/python_keywords.txt"
        self.run_parser()
        expected_keywords = ['if', 'else']
        self.assertEqual(expected_keywords, self.p.keywords)

    def test_python_literals(self):
        """
        This test is testing parser for finding all literals in python code
        """
        self.filename = "parser_tests/python_literals.txt"
        self.run_parser()
        expected_literals = ['True', 'False', 'None']
        self.assertEqual(expected_literals, self.p.literals)

    def test_find_all_operations(self):
        """
        This test is testing parser for finding all operations in python code
        """
        self.filename = "parser_tests/python_operations.txt"
        expected_operations = ['+', '-', '*', '/', '//', '%', '-', '+', '**']
        self.run_parser()
        self.assertListEqual(expected_operations, self.p.operations)

    def test_python_import(self):
        """
        This test is testing parser for finding all libraries in python code
        """
        self.filename = "parser_tests/python_imports.txt"
        self.run_parser()
        expected_keywords = ['import', 'import', 'import', 'from', 'import']
        self.assertEqual(expected_keywords, self.p.keywords)

    def test_python_libraries(self):
        """
        This test is testing parser for for finding all keywords of libraries import in python code
        """
        self.filename = "parser_tests/python_imports.txt"
        self.run_parser()
        expected_libraries = ['foo', '_foo_', 'lib.foo', 'lib', 'foo']
        self.assertEqual(expected_libraries, self.p.scanner.libraries)

    def test_ignore_one_line_comments(self):
        """
        This test is testing parser for ignore all one line comments
        """
        self.filename = "parser_tests/python_comments.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_ignore_two_lines_comments(self):
        """
        This test is testing parser for ignore all two lines comments from type 1 '''comment '''
        """
        self.filename = "parser_tests/python_2_lines_comments.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_ignore_two_lines_comments2(self):
        """
        This test is testing parser for ignore all two lines comments from type 2
        """
        self.filename = "parser_tests/python_2_lines_comments2.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_ignore_strings(self):
        """
        This test is testing parser for ignore all strings in python code
        """
        self.filename = "parser_tests/python_strings.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_run_real_code(self):
        """
        This test is testing parser for finding all keywords in real python code
        """
        self.filename = "test_result_parser.py"
        expected_keywords = ['import', 'from', 'import', 'from', 'import', 'from', 'import', 'from',
                             'import', 'class', 'def', 'def', 'in', 'def', 'def', 'print', 'in', 'def']
        self.run_parser()
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_keywords_in_function(self):
        """
        This test is testing parser for finding all keywords including inside function call in python code
        """
        self.filename = "parser_tests/test_result_parser.txt"
        expected_keywords = ['def', 'in']
        self.run_parser()
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_find_functions(self):
        """
        This test is testing parser for finding all function calls in python code
        """
        self.filename = "parser_tests/python_functions.txt"
        expected_functions = ['foo', 'foo']
        self.run_parser()
        self.assertListEqual(expected_functions, self.p.scanner.functions_calls)

    def test_find_functions_in_longer_text(self):
        """
        This test is testing parser for finding all function calls in long python code
        """
        self.filename = "parser_tests/test_result_parser.txt"
        expected_functions = ['LanguagesAPI', 'http_request_using_urlfetch', 'ResultParser',
                              'find_by_id', 'assertNotEqual']
        self.run_parser()
        self.assertListEqual(expected_functions, self.p.scanner.functions_calls)

    def test_run_real_code2(self):
        self.filename = "../translation_engine/translation_engine.py"
        self.run_parser()

    def test_classes(self):
        """
        This test is testing parser for finding all classes declarations in python code
        """
        self.filename = "parser_tests/python_classes.txt"
        expected_classes = ["foo", "foo1", "foo2"]
        self.run_parser()
        self.assertListEqual(expected_classes, self.p.scanner.classes)

    def test_find_all_func_def(self):
        """
        This test is testing parser for finding all functions declarations in python code
        """
        self.filename = "parser_tests/test_result_parser.txt"
        expected_func_def = ["test_find_by_id_get_for_statement_python"]
        self.run_parser()
        self.assertListEqual(expected_func_def, self.p.scanner.functions)

    def test_ignore_unrecognized_symbols(self):
        """
        This test is testing parser for ignoring all unrecognized symbols (as Hebrew)
        """
        self.filename = "parser_tests/python_unrecognized_symbols.txt"
        self.run_parser()
        expected_keywords = ['if', 'for']
        self.assertEqual(expected_keywords, self.p.keywords)

    def run_parser(self):
        """
        This internal function is used in all tests to read tokens using parser
        """
        self.p = Parser(self.filename, "Python")
        self.p.run_parser()
