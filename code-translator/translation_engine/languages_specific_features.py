__author__ = 'olesya'

from lib.plex import *

# ----------------------------------------- Main -----------------------------------------------------------
KEYWORD = "keyword"
STATEMENT = "statement"
LITERAL = "literal"
OPERATION = "operation"
FUNCTION = "function"
COMMENT = "comment"
STRING = "string"
DATA_TYPE = "data type"
OPERATOR = "operator"
EXPRESSION = "expression"

symbols = Str(',', '.', '_', '!', '/', '(', ')', ':', '-', '[', ']', '{', '}', '@', '%', '^', '&', '*', '=', '`', '$',
              '+', '|', '\\', '?', '<', '>')

terminate_line_symb = Str(';')

comments_symbols = Str('#', '"', "'")

str_symbol1 = '"'
str_symbol2 = "'"
default_class_keyword = Str('class')
default_function_start = '('
default_function_call_char = '('

# ----------------------------------------- Python -----------------------------------------------------------
# Keywords:
python_keywords = Str('as', 'assert', 'del', 'elif', 'else', 'except', 'exec', 'finally', 'global', 'is', 'lambda',
                      'and', 'or', 'not', 'print', 'raise', 'try', 'with', 'yield', 'in','for', 'if', 'while', 'break',
                      'continue', 'pass', 'return')

# Statements
python_statements = ['for', 'if', 'else', 'while', 'break', 'continue', 'pass', 'return']

# Literals:
python_boolean = Str('True', 'False', 'None')
# Operations:
python_operations = Str('<', '<=', '>', '>=', '=', '==', '!=', '+', '-', '*', '**', '/', '//', '%', '<>', '+=', '-=',
                        '*=', '/=', '%=', '**=', '//=', '&', '|', '^', '~', '<<', '>>')

python_data_type = []
python_operator = ['is', 'and', 'or', 'not', 'in']
python_expression = ['print', 'yield', 'lambda']

# The keywords defines library adding:
python_add_library = Str('import', 'from')
# One line comment symbol:
python_start_comment_symb = Str('#')
# 2 lines comments symbols:

python_comment_start1 = python_comment_end1 = Str("'''")
python_comment_start2 = python_comment_end2 = Str('"""')
# Function definition recognize:
python_func_def = Str('def')

python_describe_class_keyword = Str()
# ----------------------------------------- Java -----------------------------------------------------------
# Keywords:
java_keywords = Str('abstract',	'continue',	'for', 'new', 'switch', 'assert', 'default', 'goto',
                    'package', 'synchronized', 'boolean', 'do', 'if', 'this', 'break',
                    'double', 'implements', 'protected', 'throw', 'byte', 'else',
                    'throws', 'case', 'enum', 'instanceof', 'return', 'transient', 'catch',	'extends',
                    'int', 'short', 'try', 'char', 'final', 'interface', 'static', 'void',
                    'finally', 'long', 'strictfp',  'volatile', 'const', 'float', 'native', 'super',
                    'while')
# Statements
java_statements = ['for', 'if', 'else', 'while', 'break', 'continue', 'return', 'switch', 'case', 'do', 'new',
                   'assert', 'default', 'do', 'throw', 'throws', 'catch', 'try', 'void', 'finally']
# Data types
java_data_type = ['double', 'int', 'char', 'boolean', 'float', 'long', 'byte', 'short', 'enum']

# Operators
java_operator = ['instanceof']

# Literals:
java_boolean = Str('true', 'false', 'null')

# Operations:
java_operations = Str('+', '-', '*', '/', '%', '++', '--',  '==', '!=', '<', '<=', '>', '>=', '=', '&', '|', '^', '~',
                      '<<', '>>', '>>>', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=', '<<=', '>>=', '&=', '^=', '|=',
                      '?', ':')

java_expressions = []

# The keywords defines library adding:
java_add_library = Str('import')
# One line comment symbol:
java_start_comment_symb = Str('//')
# 2 lines comments symbols:
java_comment_start1 = Str('/*')
java_comment_end1 = Str('*/')
# Function definition word
java_func_def = Str('public', 'private')

# class definition
java_describe_class_keyword = Str('public', 'private')

# ------------------------------------------- Ruby ---------------------------------------------------------
# Keywords:
ruby_keywords = Str('BEGIN', 'do', 'next', 'then', 'END', 'else', 'alias', 'elsif', 'not',
                    'undef', 'and', 'end', 'or', 'unless', 'begin', 'ensure', 'redo', 'until', 'break',
                    'rescue', 'when', 'case', 'for', 'retry', 'while', 'if', 'return',
                    'in', 'self', '__FILE__', 'defined?', 'module', 'super', '__LINE__', '__ENCODING__',
                    'yield', '__END__')
# Statements
ruby_statements = ['for', 'if', 'else', 'unless', 'case', 'when', 'while', 'until', 'break', 'next', 'redo', 'retry']
# Literals:
ruby_boolean = Str('true', 'false', 'nil')
# Operations:
ruby_operations = Str('+', '-', '*', '/', '%', '**', '=~', '!~', '==', '.eql?', '!=', '<', '<=', '>', '>=', '=', '<=>',
                      '===', '|', '^', '~', '<<', '>>', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=', '|=', '<<=',
                      '**=', 'equal?', '&', '?', ':', '..', '...', '::', '>>=')

ruby__data_type = []
ruby_operator = []
ruby_expressions = []

# The keywords defines library adding:
ruby_add_library = Str('require')
# One line comment symbol:
ruby_start_comment_symb = Str('#')
# 2 lines comments symbols:
ruby_comment_start = Str('=begin')
ruby_comment_end = Str('=end')
ruby_escape_string_character = Str("\'")
ruby_func_def = Str('def')

# -----------------------------------------------------------------------------------------------------------
languages_statements = {"Java": java_statements,
                        "Python": python_statements,
                        "Ruby": ruby_statements}

languages_data_types = {"Java": java_data_type,
                        "Python": python_data_type,
                        "Ruby": ruby__data_type}
languages_operators = {"Java": java_operator,
                       "Python": python_operator,
                       "Ruby": ruby_operator}

languages_keywords = {"Java": java_keywords,
                      "Python": python_keywords,
                      "Ruby": ruby_keywords}

languages_literals = {"Java": java_boolean,
                      "Python": python_boolean,
                      "Ruby": ruby_boolean}

languages_expressions = {"Java": java_expressions,
                         "Python": python_expression,
                         "Ruby": ruby_expressions}

languages_operations = {"Java": java_operations,
                        "Python": python_operations,
                        "Ruby": ruby_operations}

languages_add_library = {"Java": java_add_library,
                         "Python": python_add_library,
                         "Ruby": ruby_add_library}

languages_start_comment_symb = {"Java": java_start_comment_symb,
                                "Python": python_start_comment_symb,
                                "Ruby": ruby_start_comment_symb}

languages_comment_start1 = {"Java": java_comment_start1,
                            "Python": python_comment_start1,
                            "Ruby": ruby_comment_start}

languages_comment_end1 = {"Java": java_comment_end1,
                          "Python": python_comment_end1,
                          "Ruby": ruby_comment_end}

languages_comment_start2 = {"Java": java_comment_start1,
                            "Python": python_comment_start2,
                            "Ruby": ruby_comment_start}

languages_comment_end2 = {"Java": java_comment_end1,
                          "Python": python_comment_end2,
                          "Ruby": ruby_comment_end}

languages_str_symbol1 = {"Java": str_symbol1,
                         "Python": str_symbol1,
                         "Ruby": str_symbol1}

languages_str_symbol2 = {"Java": str_symbol2,
                         "Python": str_symbol2,
                         "Ruby": str_symbol2}

languages_func_def = {"Java": java_func_def,
                      "Python": python_func_def,
                      "Ruby": ruby_func_def}

languages_func_start = {"Java": default_function_start,
                        "Python": default_function_start,
                        "Ruby": ""}

languages_class_keyword = {"Java": default_class_keyword,
                           "Python": default_class_keyword,
                           "Ruby": default_class_keyword}

languages_escape_character = {"Java": Str(),
                              "Python": Str(),
                              "Ruby": ruby_escape_string_character}

languages_function_call_char = {"Java": default_function_call_char,
                                "Python": default_function_call_char,
                                "Ruby": default_function_call_char}

languages_function_call_must_char = {"Java": True,
                                     "Python": True,
                                     "Ruby": False}

# Supported languages:
languages = ["Java", "Python", "Ruby"]

python_symbols_url = "http://www.tutorialspoint.com/python/python_basic_operators.htm"
java_symbols_url = "http://www.tutorialspoint.com/java/java_basic_operators.htm"
ruby_symbols_url = "http://www.tutorialspoint.com/ruby/ruby_operators.htm"


default_urls = {"Python":["https://wiki.python.org", "http://www.tutorialspoint.com/python", "https://docs.python.org/"],
                "Java": ["https://docs.oracle.com/javase/", "http://www.tutorialspoint.com/java/",
                         "http://www.codejava.net/", "http://docs.oracle.com/javase/"],
                "Ruby": ["http://www.tutorialspoint.com/"]}

url_info = {"https://wiki.python.org": {"id": "content"},
            "http://www.tutorialspoint.com": {"class": "col-md-7 middle-col"},
            "http://docs.oracle.com/javase/": {"id": "PageContent"},
            "https://docs.python.org/": {"class": "section"},
            "https://docs.oracle.com/javase/": {"id": "PageContent"},
            "http://www.codejava.net/": {"id": "content"}}
