__author__ = 'olesya'

from languages_specific_features import *


class PythonScanner(Scanner):
    libraries = []

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

    symbols = Str(',', '.', '_', '!', '/', '(', ')', ';', ':', '-', '[', ']', '{', '}', '@', '%', '^', '&',
                  '*', '=', ' ', '`', '$', '+', '|', '\\', '?', '<', '>')

    comments_symbols = Str('#', '"', "'")

    string_symbol = Str('"', "'")

    all_symbols = symbols | comments_symbols | string_symbol

    start_comment_symb = Str('#')

    new_line = Str('\n')

    escaped_newline = Str("\\\n")

    ADD_LIBRARY = Str('import', 'from')

    letter = Range("AZaz")
    digit = Range("09")
    number = Rep1(digit)

    word = Rep1(letter | number | Any('._'))

    comments_words = Rep1(letter | number | Any('._') | all_symbols)

    cm1 = Str("'''")
    cm2 = Str('"""')

    name = Rep1(letter | number | symbols)

    lexicon = Lexicon([
        (cm1,            start_comments),            #first kind multiply line comments
            State('comments', [
            (comments_words,    "word"),
            (cm1,        start_comments),
            (Rep1(Any(" \t\n")), IGNORE)
        ]),

        (cm2,         start_comments),
            State('comments2', [                            #second kind multiply line comments
            (comments_words,          "word"),
            (cm2,        start_comments),
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
            (Str(',', ' '),        IGNORE),
            (Eol | Str(";"),    Begin('')),
        ]),
        (word,              IGNORE),
        (Rep1(Any(" \t\n")), IGNORE)
    ])


    def __init__(self, file):
        Scanner.__init__(self, self.lexicon, file)
        self.indentation_stack = [0]
        self.com = False
        self.bracket_nesting_level = 0
        self.begin('')
