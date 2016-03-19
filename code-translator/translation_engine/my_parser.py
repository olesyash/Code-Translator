__author__ = 'olesya'

from languages_specific_features import *
from lib.plex.traditional import *


class PythonScanner(Scanner):
    def recognize_class(self, class_keyword):
        self.produce("keyword", class_keyword)
        self.begin('lib')

    def save_class(self, class_name):
        self.produce("class_name", class_name)
        self.classes.append(class_name)

    def save_libraries(self, lib):
      #  print "in save"
        self.libraries.append(lib)
        self.produce("lib", lib)

    def recognize_lib(self, lib):
      #  print "in recognize"
        self.produce("keyword", lib)
        self.begin('lib')

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
       # self.cur_char = text
        self.begin("functions")

    def add_function(self, text):
        print("in add functon" + text)
        print "current " + self.cur_char
        self.produce("function", self.func_name)
        print "current " + self.cur_char
        self.functions.append(self.func_name)
        print "current " + self.cur_char
        self.start_pos = self.cur_pos
        self.begin('')

        #self.begin("arguments")

    def back_to_init(self, text):
        print("BACK TO INIT" + text)
        print(self.cur_char)
        self.start_pos = self.cur_pos
        self.begin('')

    def recognize_string(self, text):
        print("in string " + text)
        self.produce("string", text)

    symbols = Str(',', '.', '_', '!', '/', '(', ')', ';', ':', '-', '[', ']', '{', '}', '@', '%', '^', '&',
                  '*', '=', ' ', '`', '$', '+', '|', '\\', '?', '<', '>')

    comments_symbols = Str('#', '"', "'")


    start_comment_symb = Str('#')

    new_line = Str('\n')

    escaped_newline = Str("\\\n")

    ADD_LIBRARY = Str('import', 'from')

    CLASS_KEYWORD = Str('class')

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
        (string_word1 | string_word2,        recognize_string),
        (cm1,            start_comments),            #first kind multiply line comments
            State('comments', [
            (cm1,        start_comments),
            (comments_words,    "word"),
            (Rep1(Any(" \t\n")), IGNORE)
        ]),

        (cm2,         start_comments),
            State('comments2', [                     #second kind multiply line comments
            (cm2,        start_comments),
            (comments_words,     IGNORE),
            (Rep1(Any(" \t\n")), IGNORE)
        ]),


        (python_keywords,    "keyword"),                    #Catch all keywords
        (symbols | string_symbol,             IGNORE),      #Ignore symbols
        (start_comment_symb,  Begin('comment')),            #Ignore one line comments
        State('comment', [
            (Eol,            Begin('')),
            (name | all_symbols,            IGNORE)

        ]),

        (number,              IGNORE),                      #Ignore numbers
        (ADD_LIBRARY,         recognize_lib),               #Catch all libraries
        State('lib', [
            (ADD_LIBRARY,     "keyword"),
            (word,            save_libraries),
            (Str(',', ' ', '*'),        IGNORE),
            (Eol | Str(";"),    Begin('')),
        ]),
        #(word,                  TEXT),
        (word,               check_call_function),
        State('functions', [
            (Str('('),    add_function),
            (AnyBut('('), back_to_init)

        ]),

        (Rep1(Any(" \t\n")), IGNORE)
    ])

    def __init__(self, file):
        Scanner.__init__(self, self.lexicon, file)
        self.libraries = []
        self.functions = []
        self.classes = []
        self.func_name = ""
        self.indentation_stack = [0]
        self.com = False
        self.bracket_nesting_level = 0
        self.begin('')

