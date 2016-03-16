__author__ = 'olesya'


from lib.plex import *

python_keywords = Str('and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec',
                   'finally', 'for', 'global', 'if', 'in', 'is', 'lambda', 'not', 'or', 'pass',
                   'print', 'raise', 'return', 'try', 'while', 'with', 'yield')

simple_conditions = ['<', '>', '=', '*']
bool = ['True', 'False']

conditional_expressions = ['<=', '>=', '==', '!=']

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

default_urls = {
    "Python": "https://wiki.python.org",
    "Java": "https://docs.oracle.com"
}
'''