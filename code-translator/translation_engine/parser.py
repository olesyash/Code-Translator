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

    def start_comment(self, a, token):
        """
        This function called when comment starts
        Start state "comment"
        """
        self.produce("comment", token)
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
            self.produce(FUNCTION, text)
            self.functions_calls.append(text)
        elif not self.must_func_call_char:
            if text in self.functions:
                self.produce(FUNCTION, text)
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
            all_data = LanguagesSpecificFeatures(self.language)
            all_keywords = all_data.prepare_for_lexicon("keywords")
            str_symbol1 = all_data.prepare_for_lexicon("str_symbol1")
            str_symbol2 = all_data.prepare_for_lexicon("str_symbol2")
            operations = all_data.prepare_for_lexicon("operations")
            add_library = all_data.prepare_for_lexicon("add_library")
            literals = all_data.prepare_for_lexicon("literals")
            start_comment_symb = all_data.prepare_for_lexicon("start_comment_symb")
            comment_start1 = all_data.prepare_for_lexicon("comment_start1")
            comment_start2 = all_data.prepare_for_lexicon("comment_start2")
            comment_end1 = all_data.prepare_for_lexicon("comment_end1")
            comment_end2 = all_data.prepare_for_lexicon("comment_end2")
            func_def = all_data.prepare_for_lexicon("func_def")
            class_keyword = all_data.prepare_for_lexicon("class_keyword")
            escape_character = all_data.prepare_for_lexicon("escape_character")
            self.func_start = all_data.prepare_for_lexicon("func_start")
            self.func_call_char = all_data.prepare_for_lexicon("function_call_char")
            self.must_func_call_char = all_data.prepare_for_lexicon("function_call_must_char")
            self.need_func_start = self.func_start != ""
            if self.debug:
                logging.info(all_keywords)
                logging.info(str_symbol1)
                logging.info(str_symbol2)
                logging.info(operations)
                logging.info(add_library)
                logging.info(start_comment_symb)
                logging.info(comment_start1)
                logging.info(comment_start2)
                logging.info(comment_end1)
                logging.info(comment_end2)
                logging.info(func_def)
                logging.info(class_keyword)
                logging.info(escape_character)
                logging.info(self.func_start)
                logging.info(self.func_call_char)
                logging.info(self.must_func_call_char)
                logging.info(self.need_func_start)
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
        string_words = Rep1(letter | number | symbols | Str(" "))

        self.lexicon = Lexicon([
            # Ignore strings
            (Str(str_symbol1), Begin('string1')),
            State('string1', [
                (escape_character, STRING),
                (string_words, STRING),
                (Str(str_symbol1), Begin('')),
            ]),
            (Str(str_symbol2), Begin('string2')),
            State('string2', [
                (escape_character, STRING),
                (string_words, STRING),
                (Str(str_symbol2), Begin('')),
            ]),

            # Ignore first kind multiply line comments
            (comment_start1, self.start_comments),
            State('comments', [
                (comment_end1, self.start_comments),
                (comments_words, COMMENT),
                (Rep1(Any(" \t\n")), IGNORE)
            ]),

            # Ignore second kind multiply line comments
            (comment_start2, self.start_comments),
            State('comments2', [
                (comment_end2, self.start_comments),
                (comments_words, COMMENT),
                (Rep1(Any(" \t\n")), IGNORE)
            ]),

            # Find all keywords in code
            (all_keywords, KEYWORD),

            # Find all literals in code
            (literals, LITERAL),

            # Find all operations
            (operations, OPERATOR),

            # Ignore symbols
            (terminate_line_symb, IGNORE),
            (symbols | string_symbol, IGNORE),

            # Ignore one line comments
            (start_comment_symb, self.start_comment),
            State('comment', [
                (Eol, Begin('')),
                (name | all_symbols | Str(" "), COMMENT)

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
        self.debug = False
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
        self.keywords = []
        self.operations = []
        self.literals = []
        self.full_list = {}
        self.list_of_tuples = []

    def run_parser(self, code_text):
        """
        This internal function is used in all tests to read tokens using parser
        """
        stream = io.TextIOWrapper(io.BytesIO(code_text), encoding="utf8")
        self.scanner = MyScanner(stream, self.language)
        self.scanner.libraries = []

        while 1:
            logging.info("in parser, starting while")
            token = self.scanner.read()
            logging.info("in run parser, token {}".format(token))
            logging.info("in run parser, scanner position {}".format(self.scanner.position()))
            if token[0] == KEYWORD:
                self.keywords.append(token[1])
            elif token[0] == OPERATOR:
                self.operations.append(token[1])
            elif token[0] == LITERAL:
                self.literals.append(token[1])

            if token[0] is None:
                break
            elif token[0] == "unrecognized":
                pass
                # raise errors.UnrecognizedInput(self.scanner, '')
            elif token[0] == COMMENT or token[0] == STRING:
                parsed = (token[0], token[1], self.scanner.position())
                self.list_of_tuples.append(parsed)
            else:
                self.full_list[token[1]] = token[0]
                parsed = (token[0], token[1], self.scanner.position())
                self.list_of_tuples.append(parsed)
        return self.full_list, self.list_of_tuples