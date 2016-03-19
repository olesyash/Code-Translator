__author__ = 'olesya'

from languages_specific_features import *
from lib.plex.traditional import *


class PythonScanner(Scanner):

    def recognize_function_definition(self, text):
        print "in function recognize"
        self.produce(KEYWORD, text)
        self.begin('def_func')

    def save_functions(self, func_name):
        print "int func save"
        self.produce("func_name", func_name)
        self.functions.append(func_name)

    def recognize_class(self, class_keyword):
        """
        This function called when class keyword recognized,
        Start state 'class'
        """
        print("in recognize class")
        self.produce(KEYWORD, class_keyword)
        self.begin('class')

    def save_class(self, class_name):
        print "in save class", class_name
        self.produce("class_name", class_name)
        self.classes.append(class_name)

    def recognize_lib(self, lib):
      #  print "in recognize"
        self.produce(KEYWORD, lib)
        self.begin('lib')

    def save_libraries(self, lib):
      #  print "in save"
        self.libraries.append(lib)
        self.produce("lib", lib)

    def start_comment(self):
        print("in comment")
        self.begin('comment')

    def start_comments(self, text):
        print("in comments" + text)
        print(self.bracket_nesting_level)

        if self.bracket_nesting_level == 0:
            self.bracket_nesting_level += 1
            print("start state comments")
            if text == "'''":
                self.begin("comments")
            else:
                self.begin("comments2")
        elif self.bracket_nesting_level == 1:
                self.bracket_nesting_level -= 1
                self.begin('')

    def check_call_function(self, text):
        print "check function", text
        self.func_name = text
        self.begin("functions")

    def add_function(self, text):
        print("in add functon" + text)
        print "current " + self.cur_char
        self.produce("function", self.func_name)
        print "current " + self.cur_char
        self.functions_calls.append(self.func_name)
        print "current " + self.cur_char
        self.start_pos = self.cur_pos
        self.begin('')

    def back_to_init(self, text):
        print("BACK TO INIT" + text)
        print(self.cur_char)
        self.start_pos = self.cur_pos
        self.begin('')

    def recognize_string(self, text):
        print("in string " + text)
        self.produce("string", text)

    def ignore_all(self, text):
        print "in ignore", text
        self.begin('ignore')

    symbols = Str(',', '.', '_', '!', '/', '(', ')', ';', ':', '-', '[', ']', '{', '}', '@', '%', '^', '&',
                  '*', '=', ' ', '`', '$', '+', '|', '\\', '?', '<', '>')

    comments_symbols = Str('#', '"', "'")


    start_comment_symb = Str('#')

    new_line = Str('\n')

    escaped_newline = Str("\\\n")

    ADD_LIBRARY = Str('import', 'from')

    CLASS_KEYWORD = Str('class')

    FUNC_DEF = Str('def')

    letter = Range("AZaz")
    digit = Range("09")
    number = Rep1(digit)

    word = Rep1(letter | number | Any('._'))

    cm1 = Str("'''")
    cm2 = Str('"""')

    name = Rep1(letter | number | symbols) | Empty

    str_symbol1 = Str('"')
    str_symbol2 = Str("'")

    # string_word1 = str_symbol1 + re('[^"]') + str_symbol1
    # string_word2 = str_symbol2 + re("[^']") + str_symbol2
    string_word1 = str_symbol1 + (Rep(Rep(name) |symbols | start_comment_symb) | Rep(str_symbol2)) + str_symbol1
    string_word2 = str_symbol2 + (Rep(Rep(name) |symbols | start_comment_symb) | Rep(str_symbol1)) + str_symbol2

    string_symbol = str_symbol1 | str_symbol2

    all_symbols = symbols | comments_symbols | string_symbol
    comments_words = Rep1(letter | number | Any('._') | all_symbols)



    lexicon = Lexicon([
        # Ignore strings
        (string_word1 | string_word2,        recognize_string),

        # Ignore first kind multiply line comments
        (cm1,            start_comments),
            State('comments', [
            (cm1,        start_comments),
            (comments_words,    "word"),
            (Rep1(Any(" \t\n")), IGNORE)
        ]),

        # Ignore second kind multiply line comments
        (cm2,         start_comments),
            State('comments2', [
            (cm2,        start_comments),
            (comments_words,     IGNORE),
            (Rep1(Any(" \t\n")), IGNORE)
        ]),

        # Find all keywords in code
        (python_keywords,    KEYWORD),

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
        (ADD_LIBRARY,         recognize_lib),

        # Find all libraries in code
        State('lib', [
            (ADD_LIBRARY,     KEYWORD),
            (word,            save_libraries),
            (Str(',', ' ', '*'),        IGNORE),
            (Eol | Str(";"),    Begin('')),
        ]),

        # Find classes
        (CLASS_KEYWORD,        recognize_class),
        State('class', [
           # (CLASS_KEYWORD,    KEYWORD),
            (word,              save_class),
            (AnyBut('(:'),      IGNORE),
            (Str(':'),          Begin('')),
            (Str('('),          ignore_all),
        ]),
        (FUNC_DEF,              recognize_function_definition),
        State('def_func', [
            (word,              save_functions),
            (AnyBut('(:'),     IGNORE),
            (Str(':'),         Begin('')),
            (Str('('),         ignore_all),

        ]),

        # Ignore all inside brackets() in class and function declaration
        State('ignore', [
            (AnyBut(':'),      IGNORE),
            (Str(':'),          Begin('')),
        ]),

        # Find all functions calls
        (word,               check_call_function),
        State('functions', [
            (Str('('),    add_function),
            (AnyBut('('), back_to_init)

        ]),

        # Ignore all indentations and new lines
        (Rep1(Any(" \t\n")), IGNORE)
    ])

    def __init__(self, file):
        Scanner.__init__(self, self.lexicon, file)
        self.libraries = []
        self.functions = []
        self.functions_calls = []
        self.classes = []
        self.func_name = ""
        self.bracket_nesting_level = 0
        self.begin('')

