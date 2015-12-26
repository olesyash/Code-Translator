__author__ = 'olesya'


def get_statements(language):
    if language == "python":
        return python_statements
    elif language == "java":
        return java_statements


python_statements = ['for', 'if', 'else', 'while']
java_statements = ['for', 'if', 'else', 'while']

default_urls = {
    "python": "https://wiki.python.org",
    "java": "https://docs.oracle.com"
}
