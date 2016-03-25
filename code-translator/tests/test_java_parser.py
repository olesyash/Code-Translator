__author__ = 'olesya'

import unittest
from translation_engine.my_parser import *

# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)


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

    def run_parser(self):
        """
        This internal function is used in all tests to read tokens using parser
        """
        self.p = Parser(self.filename, "Java")
        self.p.run_parser()
