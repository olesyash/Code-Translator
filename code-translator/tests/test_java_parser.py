__author__ = 'olesya'

import unittest
from translation_engine.my_parser import *

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class MyParserJavaTest(unittest.TestCase):
    def test_java_keywords(self):
        """
        This test is testing parser for finding all keywords in java code
        """
        self.filename = "parser_tests/java_keywords.txt"
        self.run_parser()
        expected_keywords = ['import', 'public', 'class', 'extends', 'private', 'static', 'final', 'int', 'private',
                             'private', 'int', 'public', 'int', 'int', 'int', 'int', 'int', 'double', 'super']
        self.assertEqual(expected_keywords, self.p.keywords)

    def test_java_literals(self):
        """
        This test is testing parser for finding all literals in java code
        """
        self.filename = "parser_tests/java_literals.txt"
        self.run_parser()
        expected_literals = ['true', 'false', 'null']
        self.assertEqual(expected_literals, self.p.literals)

    def test_find_all_operations(self):
        """
        This test is testing parser for finding all operations in python code
        """
        self.filename = "parser_tests/java_operations.txt"
        expected_operations = ['+', '-', '*', '/', '%', '-', '+', '++', '--',  '==',
                               '!=', '<', '<=', '>']
        self.run_parser()
        self.assertListEqual(expected_operations, self.p.operations)

    def test_java_import(self):
        """
        This test is testing parser for finding all libraries in java code
        """
        self.filename = "parser_tests/java_imports.txt"
        self.run_parser()
        expected_keywords = ['import', 'import', 'import']
        self.assertEqual(expected_keywords, self.p.keywords)

    def test_java_libraries(self):
        """
        This test is testing parser for for finding all keywords of libraries import in java code
        """
        self.filename = "parser_tests/java_imports.txt"
        self.run_parser()
        expected_libraries = ['java.awt.Color', 'java.awt.Graphics2D', 'java.awt.image.BufferedImage']
        self.assertEqual(expected_libraries, self.p.scanner.libraries)

    def test_ignore_one_line_comments(self):
        """
        This test is testing parser for ignore all one line comments
        """
        self.filename = "parser_tests/java_comments.txt"
        self.run_parser()
        expected_keywords = []
        expected_op = []
        self.assertListEqual(expected_op, self.p.operations)
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_ignore_two_lines_comments(self):
        """
        This test is testing parser for ignore all two lines comments from type 1 '''comment '''
        """
        self.filename = "parser_tests/java_2_lines_comments.txt"
        self.run_parser()
        expected_keywords = []
        expected_op = []
        self.assertListEqual(expected_op, self.p.operations)
        self.assertListEqual(expected_keywords, self.p.keywords)

    def run_parser(self):
        """
        This internal function is used in all tests to read tokens using parser
        """
        self.p = Parser(self.filename, "Java")
        self.p.run_parser()
