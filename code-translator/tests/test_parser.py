__author__ = 'olesya'

import unittest
from translation_engine.my_parser import *

# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

class MyParserPythonTest(unittest.TestCase):
    def test_python_import(self):
        self.filename = "parser_tests/python_imports.txt"
        self.run_parser()
        #print("all libraries: ")
        #print(self.scanner.libraries)
        expected_libraries = ['foo', '_foo_', 'lib.foo', 'lib', 'foo']
        self.assertEqual(expected_libraries, self.scanner.libraries)

    def test_python_libraries(self):
        self.filename = "parser_tests/python_imports.txt"
        self.run_parser()
        expected_keywords = ['import', 'import', 'import', 'from', 'import']
        self.assertEqual(expected_keywords, self.keywords)

    def test_python_keywords(self):
        self.filename = "parser_tests/python_keywords.txt"
        self.run_parser()
        expected_keywords = ['if', 'else']
        self.assertEqual(expected_keywords, self.keywords)

    def test_ignore_one_line_comments(self):
        self.filename = "parser_tests/python_comments.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.keywords)

    def test_ignore_two_lines_comments(self):
        self.filename = "parser_tests/python_2_lines_comments.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.keywords)

    def test_ignore_two_lines_comments2(self):
        self.filename = "parser_tests/python_2_lines_comments2.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.keywords)

    def test_ignore_strings(self):
        self.filename = "parser_tests/python_strings.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.keywords)

    def test_negative_ignore_strings(self):
        self.filename = "parser_tests/python_imports.txt"
        self.run_parser()
        expected_keywords = []
        self.assertNotEqual(expected_keywords, self.keywords)

    def test_run_real_code(self):
        self.filename = "test_result_parser.py"
        expected_keywords = ['import', 'from', 'import', 'from', 'import', 'from', 'import', 'from',
                             'import', 'class', 'def', 'def', 'in', 'def', 'def', 'print', 'in', 'def']
        self.run_parser()
        self.assertListEqual(expected_keywords, self.keywords)

    def test_keywords_in_function(self):
        self.filename = "parser_tests/test_result_parser.txt"
        expected_keywords = ['def']
        self.run_parser()
        self.assertListEqual(expected_keywords, self.keywords)

    def test_find_functions(self):
        self.filename = "parser_tests/python_functions.txt"
        expected_functions = ['foo', 'a.foo']
        self.run_parser()
        self.assertListEqual(expected_functions, self.scanner.functions_calls)

    def test_find_functions_in_longer_text(self):
        self.filename = "parser_tests/test_result_parser.txt"
        expected_functions = ['LanguagesAPI', 'a.http_request_using_urlfetch', 'ResultParser',
                              'b.find_by_id', 'self.assertNotEqual']
        self.run_parser()
        self.assertListEqual(expected_functions, self.scanner.functions_calls)

    def test_run_real_code2(self):
        self.filename = "../translation_engine/translation_engine.py"
        self.run_parser()

    def test_classes(self):
        self.filename = "parser_tests/python_classes.txt"
        expected_classes = ["foo", "foo1", "foo2"]
        self.run_parser()
        self.assertListEqual(expected_classes, self.scanner.classes)

    def test_find_all_func_def(self):
        self.filename = "parser_tests/test_result_parser.txt"
        expected_func_def = ["test_find_by_id_get_for_statement_python"]
        self.run_parser()
        self.assertListEqual(expected_func_def, self.scanner.functions)

    def test_find_all_operations(self):
        self.filename = "parser_tests/python_operations.txt"
        expected_operations = ['+', '-', '*', '/', '//', '%', '-', '+', '**']
        self.run_parser()
        self.assertListEqual(expected_operations, self.operations)

    def test_ignore_unrecognized_symbols(self):
        self.filename = "parser_tests/python_unrecognized_symbols.txt"
        self.run_parser()
        expected_keywords = ['if', 'for']
        self.assertEqual(expected_keywords, self.keywords)

    def run_parser(self):
        f = open(self.filename, "r")
        self.keywords = []
        self.operations = []

        self.scanner = PythonScanner(f)
        self.scanner.libraries = []
        while 1:
            token = self.scanner.read()
            print token
            print self.scanner.position()
            if token[0] == "keyword":
                self.keywords.append(token[1])
            elif token[0] == "operation":
                self.operations.append(token[1])
            if token[0] is None:
                break
