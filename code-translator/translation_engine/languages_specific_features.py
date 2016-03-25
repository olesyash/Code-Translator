__author__ = 'olesya'

from lib.plex import *

# ----------------------------------------- Main -----------------------------------------------------------
KEYWORD = "keyword"

symbols = Str(',', '.', '_', '!', '/', '(', ')', ';', ':', '-', '[', ']', '{', '}', '@', '%', '^', '&',
              '*', '=', ' ', '`', '$', '+', '|', '\\', '?', '<', '>')

comments_symbols = Str('#', '"', "'")
#----------------------------------------- Python -----------------------------------------------------------

python_keywords = Str('and', 'as', 'assert', 'break', 'continue', 'del', 'elif', 'else', 'except', 'exec',
                      'finally', 'for', 'global', 'if', 'in', 'is', 'lambda', 'not', 'or', 'pass',
                      'print', 'raise', 'return', 'try', 'while', 'with', 'yield')


python_operations = Str('<', '<=', '>', '>=', '=', '==', '!=', '+', '-', '*', '/', '//', '%', '**')


boolean = ['True', 'False', 'None']

# ----------------------------------------- Java -----------------------------------------------------------

java_keywords = Str('abstract',	'continue',	'for', 'new', 'switch', 'assert', 'default', 'goto',
                    'package', 'synchronized', 'boolean', 'do', 'if', 'private', 'this', 'break',
                    'double', 'implements', 'protected', 'throw', 'byte', 'else', 'import', 'public',
                    'throws', 'case', 'enum', 'instanceof', 'return', 'transient', 'catch',	'extends',
                    'int', 'short', 'try', 'char', 'final', 'interface', 'static', 'void', 'class',
                    'finally', 'long', 'strictfp',  'volatile', 'const', 'float', 'native', 'super',
                    'while')

java_operations = Str()
# --------------------------------------------------------------------------------------------------------
languages_keywords = {"Java": java_keywords,
                      "Python": python_keywords}

languages_operations = {"Java": java_operations,
                        "Python": python_operations}

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
default_urls = {
    "Python": "https://wiki.python.org",
    "Java": "https://docs.oracle.com"
}
