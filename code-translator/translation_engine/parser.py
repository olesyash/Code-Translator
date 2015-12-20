__author__ = 'olesya'
from languages_specific_features import *


class Parser():

    @staticmethod
    def parse_text(code_text):
        keywords_list = list()
        words_list = code_text.split()
        for word in words_list:
            if word in python_keywords:
                keywords_list.append(word)
        return keywords_list

