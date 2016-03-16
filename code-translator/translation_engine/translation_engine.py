__author__ = 'olesya'
from my_parser import Parser
from DAL import *
import logging
from lib.pygoogle import pygoogle
from languages_specific_features import *
from engine.result_parser import *
from engine.languages_API import *
import re
import time
'''
Getting code from web side and using 3 steps before giving result back to web side
1. Use Parser to isolate which words should be "translated"
2. Use specific language api treatment to access needed API
3. Use specific language result parser to get the right result
'''


class TranslationEngine():

    def __init__(self, language):
        self.language = language
        self.parser_obj = Parser(self.language)

    def get_translation(self, code_text):
        """
        The function get text from web client and returns list of dictionaries describing translated words
        :param code_text : text
        :returns translated_list : list
        """
        logging.info("Got request from client " + code_text)
        translated_list = []
        keywords_list = self.parser_obj.parse_text(code_text)
        for word in keywords_list:
            logging.info("in keywords")
            try:
                logging.info("Found in DB")
                translated_list.append(DAL.get_data_from_db(word, self.language))
            except DataNotExistException:
                logging.info("Not found in DB")
                word_type = self.parser_obj.get_word_type(word)
                res = self.add_keyword(word, word_type)
                if res:
                    translated_list.append(res)
        return translated_list

    def add_keyword(self, keyword, word_type):
        """
        This functions add new keywords to DB, after searching in google
        :param keyword: string
        :param word_type: string
        """
        url = self.google_search_by_default_site(keyword, word_type)
        logging.info("URL" + url)
        la = LanguagesAPI()
        try:
            result, code = la.http_request_using_urlfetch(http_url=url)
        except WrongURL:
            url = self.google_search(keyword, word_type)
            try:
                result, code = la.http_request_using_urlfetch(http_url=url)
            except WrongURL:
                result = None
        if result is not None:
            rp = ResultParser(self.language)
            translation = rp.find_by_default_id(result)
            if not translation:
                translation = rp.strip_text_from_html(result)

            try:
                data = DAL.save_data_in_db(self.language, keyword, word_type, url, translation, approved=False)
                logging.info("Saving in DB new translation")
                return data
            except DataExistException:
                logging.info("Data already saved in db")
        else:
            return None

    def google_search_by_default_site(self, keyword, word_type):
        """
        Search in google for keyword, returns first url of website with answer.
        Search in google using "site:" option, making google to search in specific site
        :param keyword: string
        :return: url
        :rtype : string
        """
        s = self.language + " " + keyword + word_type + " site:" + default_urls[self.language]
        g = pygoogle(s)
        g.pages = 1
        urls = g.get_urls()
        print urls
        return urls[0]

    def google_search(self, keyword, word_type):
        """
        Search in google for keyword, returns first url of website with answer.
        :param keyword: string
        :return: url
        :rtype : string
        """
        s = self.language + " " + keyword + word_type
        g = pygoogle(s)
        g.pages = 1
        urls = g.get_urls()
        print urls
        return urls[0]