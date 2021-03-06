__author__ = 'olesya'

from lib.plex import *
from DAL import DAL
import logging
import json

# ----------------------------------------- Main -----------------------------------------------------------
KEYWORD = "keyword"
STATEMENT = "statement"
LITERAL = "literal"
FUNCTION = "function"
COMMENT = "comment"
STRING = "string"
DATA_TYPE = "data type"
OPERATOR = "operator"
EXPRESSION = "expression"

symbols_without_escape = Str(',', '.', '_', '!', '/', '(', ')', ':', '-', '[', ']', '{', '}', '@', '%', '^', '&', '*',
                             '=', '`', '$', '+', '|', '?', '<', '>')
escape_char = "\\"

symbols = symbols_without_escape | Str(escape_char)

terminate_line_symb = Str(';')

comments_symbols = Str('#', '"', "'")

str_symbol1 = '"'
str_symbol2 = "'"
default_class_keyword = Str('class')
default_function_start = '('
default_function_call_char = '('

# ----------------------------------------- Python -----------------------------------------------------------
# Keywords:
python_keywords = ['as', 'assert', 'del', 'elif', 'else', 'except', 'exec', 'finally', 'global', 'is', 'lambda',
                   'and', 'or', 'not', 'print', 'raise', 'try', 'with', 'yield', 'in', 'for', 'if', 'while',
                   'break', 'continue', 'pass', 'return']

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
java_keywords = ['abstract', 'continue',	'for', 'new', 'switch', 'assert', 'default', 'goto',
                 'package', 'synchronized', 'boolean', 'do', 'if', 'this', 'break',
                 'double', 'implements', 'protected', 'throw', 'byte', 'else',
                 'throws', 'case', 'enum', 'instanceof', 'return', 'transient', 'catch',	'extends',
                 'int', 'short', 'try', 'char', 'final', 'interface', 'static', 'void',
                 'finally', 'long', 'strictfp',  'volatile', 'const', 'float', 'native', 'super',
                 'while']
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
ruby_keywords = ['BEGIN', 'do', 'next', 'then', 'END', 'else', 'alias', 'elsif', 'not',
                 'undef', 'and', 'end', 'or', 'unless', 'begin', 'ensure', 'redo', 'until', 'break',
                 'rescue', 'when', 'case', 'for', 'retry', 'while', 'if', 'return',
                 'in', 'self', '__FILE__', 'defined?', 'module', 'super', '__LINE__', '__ENCODING__',
                 'yield', '__END__']
# Statements
ruby_statements = ['for', 'if', 'else', 'unless', 'case', 'when', 'while', 'until', 'break', 'next', 'redo', 'retry',
                   'do', 'then', 'END', 'alias', 'undef', 'return', 'yield']
# Literals:
ruby_boolean = Str('true', 'false', 'nil')
# Operations:
ruby_operations = Str('+', '-', '*', '/', '%', '**', '=~', '!~', '==', '.e  ql?', '!=', '<', '<=', '>', '>=', '=', '<=>',
                      '===', '|', '^', '~', '<<', '>>', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=', '|=', '<<=',
                      '**=', 'equal?', '&', '?', ':', '..', '...', '::', '>>=')

ruby__data_type = []
ruby_operator = ['not', 'or', 'and']
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

languages_escape_character = {"Java": escape_char,
                              "Python": escape_char,
                              "Ruby": escape_char}

languages_func_def = {"Java": java_func_def,
                      "Python": python_func_def,
                      "Ruby": ruby_func_def}

languages_func_start = {"Java": default_function_start,
                        "Python": default_function_start,
                        "Ruby": ""}

languages_class_keyword = {"Java": default_class_keyword,
                           "Python": default_class_keyword,
                           "Ruby": default_class_keyword}

languages_function_call_char = {"Java": default_function_call_char,
                                "Python": default_function_call_char,
                                "Ruby": default_function_call_char}

languages_function_call_must_char = {"Java": True,
                                     "Python": True,
                                     "Ruby": False}

# Supported languages:
languages = ["Java", "Python", "Ruby-1.9"]

python_symbols_url = "http://www.tutorialspoint.com/python/python_basic_operators.htm"
java_symbols_url = "http://www.tutorialspoint.com/java/java_basic_operators.htm"
ruby_symbols_url = "http://www.tutorialspoint.com/ruby/ruby_operators.htm"


default_urls = {"Python": ["https://docs.python.org/", "https://wiki.python.org", "http://www.tutorialspoint.com/python"],
                "Java": ["https://docs.oracle.com/javase/", "http://docs.oracle.com/javase/",
                         "http://www.tutorialspoint.com/java/", "http://www.codejava.net/"],
                "Ruby": ["http://www.tutorialspoint.com/", "http://ruby-doc.org/docs/keywords/1.9/Object.html",
                         "http://ruby-doc.org/docs/", "http://docs.ruby-lang.org/"]}

url_info = {"https://wiki.python.org": {"id": "content"},
            "http://www.tutorialspoint.com": {"class": "col-md-7 middle-col"},
            "http://docs.oracle.com/javase/": {"id": "PageContent"},
            "https://docs.python.org/": {"class": "section"},
            "https://docs.oracle.com/javase/": {"id": "PageContent"},
            "http://www.codejava.net/": {"id": "content"},
            "http://ruby-doc.org/docs/keywords/1.9/Object.html": {"class": "documentation-section"},
            "http://ruby-doc.org/docs/keywords/1.9/": {"id": "section"},
            "http://docs.ruby-lang.org/": {"all": ""}}

classifications = ["keywords", "expressions", "statements", "data_types"]


def keyword_is_title(language, keyword, title):
    """
    Check if keyword defined by a title
    :param language: string
    :param keyword: string
    :param title: string
    :return: True if keyword defined by a title, false if not
    """
    try:
        return keyword in eval("languages_" + title)[language]
    except KeyError:
        return False


def get_keyword_classification(language, keyword):
    """
    This function classify the keywords to groups
    :param language: string
    :param keyword: string
    :return: the group of the keyword e.g statement, data type and etc
    """
    if keyword_is_title(language, keyword, "statements"):
        return STATEMENT
    elif keyword_is_title(language, keyword, "data_types"):
        return DATA_TYPE
    elif keyword_is_title(language, keyword, "expressions"):
        return EXPRESSION
    elif keyword_is_title(language, keyword, "operators"):
        return OPERATOR

    return DAL.get_classification(language, keyword)


def get_urls_for_language(language):
    """
    This function return all defined urls for language
    If exist in code, return it as it. If not exist in the code, pull it from db
    :param language:
    :return:
    """
    try:
        return default_urls[language]
    except KeyError:
        print "need to search in DB"
        dal = DAL()
        urls = dal.get_language_details(language, "urls")
        return urls


def get_details_about_url(url):
    """
    This function return url details to parse it in the best way
    for example: type = id, name = content
    :param url: string
    :return: parsing type and name
    """
    for key in url_info:
        if key in url:
            return url_info[key].items()[0]
    else:
        print "need to search in DB"
        dal = DAL()
        return dal.get_url_details(url)


class LanguagesSpecificFeatures():
    def __init__(self, language):
        self.language = language
        self.dal = DAL()
        if self.language not in languages:
            self.data = self.dal.get_all_data_for_language(self.language)
            logging.info("self data:")
            logging.info(self.data)
            data_type = type(self.data)
            logging.info(str(data_type))
            if data_type == unicode:
                print "converting from unicode to json"
                json_load = json.loads(self.data)
                logging.info("json loads data, new type: ")
                logging.info(str(type(json_load)))
                self.data = json_load

    def find_all_keywords(self):
        """
        This function find all keywords in language
        :return: list of keywords
        """
        try:
            return languages_keywords[self.language]
        except KeyError:
            print "need to search in DB"
            if not self.data:
                return False
            return self.data["keywords"]

    def prepare_for_lexicon(self, title):
        """
        This function prepares for lexicon the needed values by executing Str() function on list
        :param title: The features of the language needed to be prepared for lexicon
        :return: Alt object
        """
        self.language = "Ruby" if self.language == "Ruby-1.9" else self.language
        try:
            res = eval("languages_" + title)[self.language]
            if title == "keywords":
                res = my_str(res)
                return res
            return res
        except KeyError:
            print "need to search in DB"
            print "title " + title
            if not self.data:
                return Str()
            res = self.data[title]
            logging.info("res: ")
            logging.info(res)
            if title == "function_call_must_char":
                return res == "True"
            if title == "escape_character":
                return res
            if title in ["str_symbol1", "str_symbol2", "function_call_char"]:
                try:
                    logging.info("prepare for lexicon title {} is ready: {}".format(title, res[0]))
                    return res[0]
                except IndexError:
                    logging.info("in except index error")
                    return my_str([])
            logging.info("prepare for lexicon title {} is ready: {}".format(title, my_str(res)))
            if res == [u'']:
                return Str()
            return my_str(res)


def get_all_languages():
    """
    This function return all languages configured in the system
    :return: list of languages
    """
    dal = DAL()
    return dal.get_all_languages()

