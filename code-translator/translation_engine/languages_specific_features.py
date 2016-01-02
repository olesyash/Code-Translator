__author__ = 'olesya'


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
