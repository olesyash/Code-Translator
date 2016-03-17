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

    def newline_action(self, text):
       # print("new line" + text)
        self.begin('')


    symbols = Str(',', '.', '_', '!', '/', '(', ')', '"', ';', ':', '-', "'", '[', ']', '{', '}', '@', '%', '^', '&',
                  '*', '=', ' ', '`', '$', '+', '|', '\\', '?', '<', '>')

    comments_symbols = Str('#', '"""', "'''")
    start_comment_symb = Str('#')
    new_line = Str('\n')
    escaped_newline = Str("\\\n")
   # any_char_but_new_line = _
    ADD_LIBRARY = Str('import', 'from')

    letter = Range("AZaz")
    digit = Range("09")
    number = Rep1(digit)

    word = Rep1(letter | number | Any('._'))

    comment1 = Str('"""') + Rep(AnyBut('"""')) + Str('"""')
    comment2 = Str("'''") + Rep(AnyBut("'''")) + Str("'''")
    comments = comment1 | comment2

    name = Rep(letter | number | symbols)

    lexicon = Lexicon([
        (python_keywords,    "keyword"),                    #Catch all keywords
        (symbols,             IGNORE),                      #Ignore symbols
        (start_comment_symb,  Begin('comment')),            #Ignore comments
        State('comment', [
            (Eol,             newline_action),
            (name | comments_symbols,            IGNORE)

        ]),
       (comments,            IGNORE),
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
        self.bracket_nesting_level = 0
        self.begin('')
