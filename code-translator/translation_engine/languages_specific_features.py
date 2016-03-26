__author__ = 'olesya'

from lib.plex import *

# ----------------------------------------- Main -----------------------------------------------------------
KEYWORD = "keyword"
LITERAL = "literal"

symbols = Str(',', '.', '_', '!', '/', '(', ')', ';', ':', '-', '[', ']', '{', '}', '@', '%', '^', '&',
              '*', '=', ' ', '`', '$', '+', '|', '\\', '?', '<', '>')

comments_symbols = Str('#', '"', "'")
#----------------------------------------- Python -----------------------------------------------------------

python_keywords = Str('as', 'assert', 'break', 'continue', 'del', 'elif', 'else', 'except', 'exec',
                      'finally', 'for', 'global', 'if', 'is', 'lambda', 'pass', 'and', 'or', 'not',
                      'print', 'raise', 'return', 'try', 'while', 'with', 'yield', 'in')

python_boolean = Str('True', 'False', 'None')

python_operations = Str('<', '<=', '>', '>=', '=', '==', '!=', '+', '-', '*', '**', '/', '//', '%',
                        '<>', '+=', '-=', '*=', '/=', '%=', '**=', '//=', '&', '|', '^', '~', '<<',
                        '>>')

python_add_library = Str('import', 'from')



# ----------------------------------------- Java -----------------------------------------------------------

java_keywords = Str('abstract',	'continue',	'for', 'new', 'switch', 'assert', 'default', 'goto',
                    'package', 'synchronized', 'boolean', 'do', 'if', 'private', 'this', 'break',
                    'double', 'implements', 'protected', 'throw', 'byte', 'else', 'public',
                    'throws', 'case', 'enum', 'instanceof', 'return', 'transient', 'catch',	'extends',
                    'int', 'short', 'try', 'char', 'final', 'interface', 'static', 'void', 'class',
                    'finally', 'long', 'strictfp',  'volatile', 'const', 'float', 'native', 'super',
                    'while')

java_boolean = Str('true', 'false', 'null')

java_operations = Str('+', '-', '*', '/', '%', '++', '--',  '==', '!=', '<', '<=', '>', '>=', '=', '&',
                      '|', '^', '~', '<<', '>>', '>>>', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=',
                      '<<=', '>>=', '&=', '^=', '|=', '?', ':')


java_add_library = Str('import')

# --------------------------------------------------------------------------------------------------------
languages_keywords = {"Java": java_keywords,
                      "Python": python_keywords}

languages_literals = {"Java": java_boolean,
                      "Python": python_boolean}

languages_operations = {"Java": java_operations,
                        "Python": python_operations}

languages_add_library = {"Java": java_add_library,
                         "Python": python_add_library}

'''
def get_statements(language):
    if language == "Python":
        return python_statements
    elif language == "Java":
        return java_statements
    else:
        return []

languages = ["Java", "Python", "C", "C++", "C#", "R", "PHP", "JS", "Ruby", "Matlab"]

python_statements = ['for', 'if', 'else', 'while']
java_statements = ['for', 'if', 'else', 'while']
'''

python_symbols_url = "https://docs.python.org/2/library/stdtypes.html#index-9"

#python_symbols_url = "http://www.tutorialspoint.com/python/python_basic_operators.htm"
#java_symbols_url = "http://www.tutorialspoint.com/java/java_basic_operators.htm"

java_symbols_url = "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/opsummary.html"

default_urls = {
    "Python": "https://wiki.python.org",
    "Java": "https://docs.oracle.com"
}
