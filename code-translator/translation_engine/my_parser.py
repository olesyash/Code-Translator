__author__ = 'olesya'

from languages_specific_features import *
from lib.plex.traditional import *
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
        logging.debug("in func save")
        logging.debug("current char " + self.cur_char)
        logging.debug("func start " + str(self.func_start))
        logging.debug( self.cur_char == str(self.func_start))
        if self.cur_char == self.func_start:
            logging.debug("curret char " + self.cur_char)

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
        self.produce("lib", lib)

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
            if text == "'''":
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
        if self.cur_char == '(':
            self.functions_calls.append(text)

    def recognize_string(self, a, text):
        """
        This function recognize string
        """
        logging.debug("in string " + text)
        self.produce("string", text)

    def ignore_all(self, a, text):
        """
        This function starts 'ignore' State. In case of class or function definition all inside brackets () need to be ignored
        """
        logging.debug("in ignore " + text)
        self.begin('ignore')

    def check_class(self, a, text):
        logging.debug(("in check class " + text))
        logging.debug(self.cur_char)

    def def_lexicon(self):
        try:
            str_symbol1 = languages_str_symbol1[self.language]
            str_symbol2 = languages_str_symbol2[self.language]
            all_keywords = languages_keywords[self.language]
            operations = languages_operations[self.language]
            add_library = languages_add_library[self.language]
            literals = languages_literals[self.language]
            start_comment_symb = languages_start_comment_symb[self.language]
            comment_start1 = languages_comment_start1[self.language]
            comment_start2 = languages_comment_start2[self.language]
            comment_end1 = languages_comment_end1[self.language]
            comment_end2 = languages_comment_end2[self.language]
            func_def = languages_func_def[self.language]
            self.func_start = languages_func_start[self.language]
            func_end = languages_func_end[self.language]
            func_ignore = languages_func_ignore[self.language]
            func_any_but = languages_func_any_but[self.language]
            describe_class_keyword = languages_describe_class_keyword[self.language]
            class_keyword = languages_class_keyword[self.language]

        except KeyError:
            print "Language not defined well"
            self.lexicon = Lexicon([])
            return


        letter = Range("AZaz")
        digit = Range("09")
        number = Rep1(digit)

        word = Rep1(letter | number | Any('_'))
        lib_name = Rep1(letter | number | Any('._'))
        name = Rep1(letter | number | symbols) | Empty

        string_word1 = str_symbol1 + (Rep(Rep(name) |symbols | start_comment_symb) | Rep(str_symbol2)) + str_symbol1
        string_word2 = str_symbol2 + (Rep(Rep(name) |symbols | start_comment_symb) | Rep(str_symbol1)) + str_symbol2

        string_symbol = str_symbol1 | str_symbol2

        all_symbols = symbols | comments_symbols | string_symbol
        comments_words = Rep1(letter | number | Any('._') | all_symbols)



        self.lexicon = Lexicon([
            # Ignore strings
            (string_word1 | string_word2,        self.recognize_string),

            # Ignore first kind multiply line comments
            (comment_start1,            self.start_comments),
                State('comments', [
                (comment_end1,        self.start_comments),
                (comments_words,    "word"),
                (Rep1(Any(" \t\n")), IGNORE)
            ]),

            # Ignore second kind multiply line comments
            (comment_start2,         self.start_comments),
                State('comments2', [
                (comment_end2,        self.start_comments),
                (comments_words,     IGNORE),
                (Rep1(Any(" \t\n")), IGNORE)
            ]),

            # Find all keywords in code
            (all_keywords,    KEYWORD),

            #Find all literals in code
            (literals,        LITERAL),

            # Find all operations
            (operations,        "operation"),

            #Ignore symbols
            (symbols | string_symbol,             IGNORE),

            #Ignore one line comments
            (start_comment_symb,  Begin('comment')),
            State('comment', [
                (Eol,            Begin('')),
                (name | all_symbols,            IGNORE)

            ]),
             #Ignore numbers
            (number,              IGNORE),
            (add_library,         self.recognize_lib),

            # Find all libraries in code
            State('lib', [
                (add_library,     KEYWORD),
                (lib_name,            self.save_libraries),
                (Str(',', ' ', '*'),        IGNORE),
                (Eol | Str(";"),    Begin('')),
            ]),

            # Find classes
           # (describe_class_keyword,        self.check_class),
            (class_keyword,        self.recognize_class),
            State('class', [
                (word,              self.save_class),
                (AnyBut('(:'),      IGNORE),
                (Str(':'),          Begin('')),
                (Str('('),          self.ignore_all),
            ]),

            # Find function definition
            (func_def,              self.recognize_function_definition),
            State('def_func', [
                (all_keywords,      KEYWORD),
                (word,              self.save_functions),
                (Rep(Any(" ")),     IGNORE)
                # (AnyBut('('),     IGNORE),
                # (Str(')'),         Begin('')),
                # (Str('('),         self.ignore_all),

            ]),

            # Ignore all inside brackets() in class and function declaration
            State('ignore', [
                (AnyBut(')'),      IGNORE),
                (Str(')'),          Begin('')),
            ]),

            # Find all functions calls
            (word,               self.check_call_function),

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
    def __init__(self, code_file, lan):
        self.language = lan
        self.filename = code_file

    def run_parser(self):
        """
        This internal function is used in all tests to read tokens using parser
        """
        f = open(self.filename, "r")
        self.keywords = []
        self.operations = []
        self.literals = []

        self.scanner = MyScanner(f, self.language)
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
            # elif token[0] == "unrecognized":
            #     raise errors.UnrecognizedInput(self.scanner, '')
            if token[0] is None:
                break
