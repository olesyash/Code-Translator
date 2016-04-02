__author__ = 'olesya'

import unittest
from translation_engine.my_parser import *

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class MyParserPythonTest(unittest.TestCase):
    def test_ruby_keywords(self):
        """
        This test is testing parser for finding all keywords in python code
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
        This test is testing parser for ignore all two lines comments from type 1 '''comment '''
        """
        self.filename = "parser_tests/ruby_2_lines_comments.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.p.keywords)

    def run_parser(self):
        """
        This internal function is used in all tests to read tokens using parser
        """
        f = open(self.filename, "r")
        output = f.read()
        self.p = Parser("Ruby")
        self.p.run_parser(output)
