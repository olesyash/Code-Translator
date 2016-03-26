__author__ = 'olesya'

from lib.plex import *

# ----------------------------------------- Main -----------------------------------------------------------
KEYWORD = "keyword"
LITERAL = "literal"

symbols = Str(',', '.', '_', '!', '/', '(', ')', ';', ':', '-', '[', ']', '{', '}', '@', '%', '^', '&',
              '*', '=', ' ', '`', '$', '+', '|', '\\', '?', '<', '>')

comments_symbols = Str('#', '"', "'")

str_symbol1 = Str('"')
str_symbol2 = Str("'")
class_keyword = Str('class')

# ----------------------------------------- Python -----------------------------------------------------------
# Keywords:
python_keywords = Str('as', 'assert', 'break', 'continue', 'del', 'elif', 'else', 'except', 'exec',
                      'finally', 'for', 'global', 'if', 'is', 'lambda', 'pass', 'and', 'or', 'not',
                      'print', 'raise', 'return', 'try', 'while', 'with', 'yield', 'in')
# Literals:
python_boolean = Str('True', 'False', 'None')
# Operations:
python_operations = Str('<', '<=', '>', '>=', '=', '==', '!=', '+', '-', '*', '**', '/', '//', '%',
                        '<>', '+=', '-=', '*=', '/=', '%=', '**=', '//=', '&', '|', '^', '~', '<<',
                        '>>')
# The keywords defines library adding:
python_add_library = Str('import', 'from')
# One line comment symbol:
python_start_comment_symb = Str('#')
# 2 lines comments symbols:
python_comment_start1 = python_comment_end1 = Str("'''")
python_comment_start2 = python_comment_end2 = Str('"""')
# Function definition recognize:
python_func_def = Str('def')
python_func_start = '('
python_ignore_state = ":"
python_func_end = Str(':')
python_any_but = '(:'
python_func_ignore = Str('(:')

python_describe_class_keyword = Str()
# ----------------------------------------- Java -----------------------------------------------------------
# Keywords:
java_keywords = Str('abstract',	'continue',	'for', 'new', 'switch', 'assert', 'default', 'goto',
                    'package', 'synchronized', 'boolean', 'do', 'if', 'this', 'break',
                    'double', 'implements', 'protected', 'throw', 'byte', 'else',
                    'throws', 'case', 'enum', 'instanceof', 'return', 'transient', 'catch',	'extends',
                    'int', 'short', 'try', 'char', 'final', 'interface', 'static', 'void', 'class',
                    'finally', 'long', 'strictfp',  'volatile', 'const', 'float', 'native', 'super',
                    'while')
# Literals:
java_boolean = Str('true', 'false', 'null')
# Operations:
java_operations = Str('+', '-', '*', '/', '%', '++', '--',  '==', '!=', '<', '<=', '>', '>=', '=', '&',
                      '|', '^', '~', '<<', '>>', '>>>', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=',
                      '<<=', '>>=', '&=', '^=', '|=', '?', ':')
# The keywords defines library adding:
java_add_library = Str('import')
# One line comment symbol:
java_start_comment_symb = Str('//')
# 2 lines comments symbols:
java_comment_start1 = Str('/*')
java_comment_end1 = Str('*/')
# Function definition word
#java_func_def = Str()
java_func_def = Str('public', 'private')
java_func_start = '('
java_func_end = Str(')')
java_ignore_state = ")"
java_any_but = '('
java_func_ignore = Str('(')

# class definition
java_describe_class_keyword = Str('public', 'private')
# --------------------------------------------------------------------------------------------------------
languages_keywords = {"Java": java_keywords,
                      "Python": python_keywords}

languages_literals = {"Java": java_boolean,
                      "Python": python_boolean}

languages_operations = {"Java": java_operations,
                        "Python": python_operations}

languages_add_library = {"Java": java_add_library,
                         "Python": python_add_library}

languages_start_comment_symb = {"Java": java_start_comment_symb,
                                "Python": python_start_comment_symb}

languages_comment_start1 = {"Java": java_comment_start1,
                            "Python": python_comment_start1}

languages_comment_end1 = {"Java": java_comment_end1,
                          "Python": python_comment_end1}

languages_comment_start2 = {"Java": java_comment_start1,
                            "Python": python_comment_start2}

languages_comment_end2 = {"Java": java_comment_end1,
                          "Python": python_comment_end2}

languages_str_symbol1 = {"Java": str_symbol1,
                         "Python": str_symbol1}

languages_str_symbol2 = {"Java": str_symbol2,
                         "Python": str_symbol2}

languages_func_def = {"Java": java_func_def,
                      "Python": python_func_def}

languages_func_start = {"Java": java_func_start,
                        "Python": python_func_start}

languages_func_ignore = {"Java": java_func_ignore,
                         "Python": python_func_ignore}

languages_func_end = {"Java": java_func_end,
                      "Python": python_func_end}

languages_func_any_but = {"Java": java_any_but,
                          "Python": python_any_but}

languages_ignore_state = {"Java": java_ignore_state,
                          "Python": python_ignore_state}

languages_class_keyword = {"Java": class_keyword,
                           "Python": class_keyword}

languages_describe_class_keyword = {"Java": java_describe_class_keyword,
                                    "Python": python_describe_class_keyword}

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
