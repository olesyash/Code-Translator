__author__ = 'olesya'

import unittest
from translation_engine.my_parser import *


class MyParserPythonTest(unittest.TestCase):
    def test_python_import(self):
        filename = "python_imports.txt"
        f = open(filename, "r")

        scanner = PythonScanner(f)
        while 1:
            token = scanner.read()
            print token
            if token[0] is None:
                break

        print("all libraries: ")
        print(scanner.libraries)
        expected_libraries = ['foo', '_foo_', 'lib.foo', 'lib', 'foo']
        self.assertEqual(expected_libraries, scanner.libraries)

