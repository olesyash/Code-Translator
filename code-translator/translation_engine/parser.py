__author__ = 'olesya'
from languages_specific_features import *


class Parser():

    def __init__(self, language):
        self.language = language
        self.statements = get_statements(language)

    def parse_text(self, code_text):
        keywords_list = list()
        words_list = code_text.split()
        for word in words_list:
            if word in self.statements:
                keywords_list.append(word)
        return keywords_list

    def get_word_type(self, word):
        if word in self.statements:
            return "statement"

