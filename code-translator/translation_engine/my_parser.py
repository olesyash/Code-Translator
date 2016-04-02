__author__ = 'olesya'

from languages_specific_features import *
from lib.plex.traditional import *
import io
import logging


class MyScanner(Scanner):
    """
    This class is inherit from scanner, for creating additional rules for scanner
    """

    def recognize_function_definition(self, a, text):
        """
        This function used to recognize function definition
        Start state 'def_func
        """
        logging.debug("in function recognize")
        self.produce(KEYWORD, text)
        logging.debug("start def_func state")
        self.begin('def_func')

    def save_functions(self, a, func_name):
        """
        This function used to save function name
        """
        logging.debug("in function save")
        if self.need_func_start and (self.cur_char != self.func_start):
            pass
        else:
            logging.debug("current char " + self.cur_char)
            self.produce("func_name", func_name)
            self.functions.append(func_name)
        self.begin('')

    def recognize_class(self, a, class_keyword):
        """
        This function called when class keyword recognized,
        Start state 'class'
        """
        logging.debug("in recognize class")
        self.produce(KEYWORD, class_keyword)
        self.begin('class')

    def save_class(self, a, class_name):
        """
        This function used to save class name
        """
        logging.debug("in save class " + class_name)
        self.produce("class_name", class_name)
        self.classes.append(class_name)
        self.begin('')

    def recognize_lib(self, a, lib):
        """
        This function called when library import keyword recognized,
        Start state 'lib'
        """
        logging.debug("in recognize lib")
        self.produce(KEYWORD, lib)
        self.begin('lib')

    def save_libraries(self, a, lib):
        """
        This function used to save library name
        """
        logging.debug("in save libraries")
        self.libraries.append(lib)
        self.produce("library", lib)

    def start_comment(self, a):
        """
        This function called when comment starts
        Start state "comment"
        """
        logging.debug("in comment")
        self.begin('comment')

    def start_comments(self, a, text):
        """
        This function called when 2 line comment starts
        Start state "comments" or "comments2" depends on comments type
        """
        logging.debug("in comments" + text)
        logging.debug(self.bracket_nesting_level)

        if self.bracket_nesting_level == 0:
            self.bracket_nesting_level += 1
            logging.debug("start state comments")
            if Str(text) == languages_comment_start1:
                self.begin("comments")
            else:
                self.begin("comments2")
        elif self.bracket_nesting_level == 1:
            self.bracket_nesting_level -= 1
            self.begin('')

    def check_call_function(self, a, text):
        """
        This function is responsible to save the word that could be function call, and start state "functions"
        """
        logging.debug("check call function " + text)

        if self.cur_char == self.func_call_char:
            self.functions_calls.append(text)
        elif not self.must_func_call_char:
            if text in self.functions:
                self.functions_calls.append(text)

    def start_string(self, a, text):
        """
        This function recognize string
        """
        logging.debug("in start string " + text)
        logging.debug("in start string char is  " + self.cur_char)
        self.begin("string")

    def escape_character_in_string(self, a, text):
        """
        This function will skip on the string symbol ending if escape character found
        """
        logging.debug("in escape character " + text)
        self.read_char()

    def check_class(self, a, text):
        logging.debug(("in check class " + text))
        logging.debug(self.cur_char)

    def def_lexicon(self):
        try:
            all_keywords = languages_keywords[self.language]
            str_symbol1 = languages_str_symbol1[self.language]
            str_symbol2 = languages_str_symbol2[self.language]
            operations = languages_operations[self.language]
            add_library = languages_add_library[self.language]
            literals = languages_literals[self.language]
            start_comment_symb = languages_start_comment_symb[self.language]
            comment_start1 = languages_comment_start1[self.language]
            comment_start2 = languages_comment_start2[self.language]
            comment_end1 = languages_comment_end1[self.language]
            comment_end2 = languages_comment_end2[self.language]
            func_def = languages_func_def[self.language]
            class_keyword = languages_class_keyword[self.language]
            escape_character = languages_escape_character[self.language]
            self.func_start = languages_func_start[self.language]
            self.func_call_char = languages_function_call_char[self.language]
            self.must_func_call_char = languages_function_call_must_char[self.language]
            self.need_func_start = self.func_start != ""
        except KeyError:
            print "Language not defined well"
            self.lexicon = Lexicon([])
            return

        letter = Range("AZaz")
        digit = Range("09")
        number = Rep1(digit)

        word = Rep1(letter | number | Any('_'))
        lib_name = Rep1(letter | number | symbols)
        name = Rep1(letter | number | symbols) | Empty

        string_symbol = Str(str_symbol1) | Str(str_symbol2)

        all_symbols = symbols | comments_symbols | string_symbol | terminate_line_symb
        comments_words = Rep1(letter | number | Any('._') | all_symbols)

        self.lexicon = Lexicon([
            # Ignore strings
            (Str(str_symbol1),       Begin('string1')),
            State('string1', [
                (AnyBut(str_symbol1),  IGNORE),
                (escape_character,     IGNORE),
                (Str(str_symbol1), Begin('')),
            ]),
            (Str(str_symbol2),       Begin('string2')),
            State('string2', [
                (AnyBut(str_symbol2),  IGNORE),
                (escape_character,     IGNORE),
                (Str(str_symbol2), Begin('')),
            ]),

            # Ignore first kind multiply line comments
            (comment_start1, self.start_comments),
            State('comments', [
                (comment_end1, self.start_comments),
                (comments_words, IGNORE),
                (Rep1(Any(" \t\n")), IGNORE)
            ]),

            # Ignore second kind multiply line comments
            (comment_start2, self.start_comments),
            State('comments2', [
                (comment_end2, self.start_comments),
                (comments_words, IGNORE),
                (Rep1(Any(" \t\n")), IGNORE)
            ]),

            # Find all keywords in code
            (all_keywords, KEYWORD),

            # Find all literals in code
            (literals, LITERAL),

            # Find all operations
            (operations, OPERATION),

            # Ignore symbols
            (terminate_line_symb,      IGNORE),
            (symbols | string_symbol, IGNORE),

            # Ignore one line comments
            (start_comment_symb, Begin('comment')),
            State('comment', [
                (Eol, Begin('')),
                (name | all_symbols | Str(" "), IGNORE)

            ]),
            # Ignore numbers
            (number, IGNORE),

            # Find all libraries in code
            (add_library, self.recognize_lib),
            State('lib', [
                (add_library, KEYWORD),
                (lib_name, self.save_libraries),
                (Str(',', ' ', '*', str_symbol1, str_symbol2), IGNORE),
                (Eol | Str(";"), Begin('')),
            ]),

            # Find classes
            (class_keyword, self.recognize_class),
            State('class', [
                (word, self.save_class),
                (Rep(Any(" ")), IGNORE)
            ]),

            # Find function definition
            (func_def, self.recognize_function_definition),
            State('def_func', [
                (class_keyword, self.recognize_class),
                (all_keywords, KEYWORD),
                (word, self.save_functions),
                (Rep(Any(" ")), IGNORE)
            ]),

            # Find all functions calls
            (word, self.check_call_function),
            # Ignore all indentations and new lines
            (Rep1(Any(" \t\n")), IGNORE)
        ])

    def __init__(self, filename, language):
        self.language = language
        self.def_lexicon()
        Scanner.__init__(self, self.lexicon, filename)
        self.libraries = []
        self.functions = []
        self.functions_calls = []
        self.classes = []
        self.prev_char = ""
        self.func_name = ""
        self.bracket_nesting_level = 0
        self.begin('')


class Parser():
    def __init__(self, lan):
        self.language = lan

    def run_parser(self, code_text):
        """
        This internal function is used in all tests to read tokens using parser
        """
        stream = io.TextIOWrapper(io.BytesIO(code_text), encoding="utf8")

        self.scanner = MyScanner(stream, self.language)
        self.keywords = []
        self.operations = []
        self.literals = []
        self.full_list = {}
        self.scanner.libraries = []

        while 1:
            token = self.scanner.read()
            print token
            print self.scanner.position()
            if token[0] == KEYWORD:
                self.keywords.append(token[1])
            elif token[0] == "operation":
                self.operations.append(token[1])
            elif token[0] == LITERAL:
                self.literals.append(token[1])
            if token[0] is None:
                break
            elif token[0] == "unrecognized":
                pass
                # raise errors.UnrecognizedInput(self.scanner, '')
            else:
                self.full_list[token[1]] = token[0]
        return self.full_list