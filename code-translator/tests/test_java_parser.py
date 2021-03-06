__author__ = 'olesya'

import unittest
from translation_engine.parser import *

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
        expected_keywords = ['import', 'public', 'class', 'extends', 'for', 'private', 'static', 'final', 'int', 'private',
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

    def test_java_find_all_operations(self):
        """
        This test is testing parser for finding all operations in java code
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

    def test_java_ignore_one_line_comments(self):
        """
        This test is testing parser for ignore all one line comments
        """
        self.filename = "parser_tests/java_comments.txt"
        self.run_parser()
        expected_keywords = []
        expected_op = []
        self.assertListEqual(expected_op, self.p.operations)
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_java_ignore_two_lines_comments(self):
        """
        This test is testing parser for ignore all two lines comments
        """
        self.filename = "parser_tests/java_2_lines_comments.txt"
        self.run_parser()
        expected_keywords = []
        expected_op = []
        self.assertListEqual(expected_op, self.p.operations)
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_java_ignore_strings(self):
        """
        This test is testing parser for ignore all strings in java code
        """
        self.filename = "parser_tests/java_strings.txt"
        self.run_parser()
        expected_keywords = []
        self.assertListEqual(expected_keywords, self.p.keywords)

    def test_java_find_all_func_def(self):
        """
        This test is testing parser for finding all functions declarations in java code
        """
        self.filename = "parser_tests/java_functions_def.txt"
        expected_func_def = ["addNotify", "startGame"]
        self.run_parser()
        self.assertListEqual(expected_func_def, self.p.scanner.functions)

    def test_java_keywords_in_func_def(self):
        """
        This test is testing parser for finding all keywords in java code
        """
        self.filename = "parser_tests/java_functions_def.txt"
        self.run_parser()
        expected_keywords = ['for', 'int', 'private', 'int', 'public', 'void', 'int', 'float', 'super', 'private', 'int', 'new', 'this']
        self.assertEqual(expected_keywords, self.p.keywords)

    def test_java_classes(self):
        """
        This test is testing parser for finding all classes declarations in java code
        """
        self.filename = "parser_tests/java_classes.txt"
        expected_classes = ["MainPanel"]
        self.run_parser()
        self.assertListEqual(expected_classes, self.p.scanner.classes)

    def test_java_find_function_calls(self):
        """
        This test is testing parser for finding all function calls in java code
        """
        self.filename = "parser_tests/java_functions.txt"
        expected_functions = ['updateSprite', 'foo', 'foo']
        self.run_parser()
        self.assertListEqual(expected_functions, self.p.scanner.functions_calls)

    def test_java_real_code(self):
        """
        This test is testing parser for finding all keywords in real java code
        """
        self.filename = "parser_tests/GameLogic.java"
        self.run_parser()
        expected_keywords = ['import', 'import', 'import', 'import', 'public', 'class', 'private', 'final', 'int',
                             'private', 'int', 'private', 'new', 'private', 'private', 'boolean', 'private', 'boolean',
                             'protected', 'private', 'private', 'private', 'private', 'private', 'private',
                             'public', 'int', 'int', 'this', 'this', 'int', 'new', 'new']
        expected_lib = ['java.awt.Graphics2D', 'java.awt.Rectangle', 'java.awt.image.BufferedImage', 'java.util.Random']
        expected_class_name = ['GameLogic']
        expected_func_def = ['GameLogic']
        expected_functions_calls = ['Random', 'pow', 'SpaceShip', 'getWidth', 'getHeight', 'createAstroids']
        self.assertEqual(expected_functions_calls, self.p.scanner.functions_calls)
        self.assertEqual(expected_func_def, self.p.scanner.functions)
        self.assertEqual(expected_class_name, self.p.scanner.classes)
        self.assertEqual(expected_lib, self.p.scanner.libraries)
        self.assertEqual(expected_keywords, self.p.keywords)

    def run_parser(self):
        """
        This internal function is used in all tests to read tokens using parser
        """
        f = open(self.filename, "r")
        output = f.read()
        self.p = Parser("Java")
        self.p.run_parser(output)
