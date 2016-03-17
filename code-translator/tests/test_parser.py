__author__ = 'olesya'

import unittest
from translation_engine.my_parser import *


class MyParserPythonTest(unittest.TestCase):
    def test_python_import(self):
        self.filename = "parser_tests/python_imports.txt"
        self.run_parser()
        print("all libraries: ")
        print(self.scanner.libraries)
        expected_libraries = ['foo', '_foo_', 'lib.foo', 'lib', 'foo']
        self.assertEqual(expected_libraries, self.scanner.libraries)

    def test_python_keywords(self):
        self.filename = "parser_tests/python_imports.txt"
        self.run_parser()
        expected_keywords = ['import', 'import', 'import', 'from', 'import']
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

    def test_run_real_code(self):
        self.filename = "test_result_parser.py"
        self.run_parser()

    def run_parser(self):
        f = open(self.filename, "r")
        self.keywords = []
        self.scanner = PythonScanner(f)
        self.scanner.libraries = []
        while 1:
            token = self.scanner.read()
            print token
            print self.scanner.position()
            if(token[0]) == "keyword":
                self.keywords.append(token[1])
            if token[0] is None:
                break