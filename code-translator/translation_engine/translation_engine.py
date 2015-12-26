__author__ = 'olesya'
from parser import Parser
from DAL import *
import logging
from lib.pygoogle import pygoogle
from languages_specific_features import *
from engine.result_parser import *
from engine.languages_API import LanguagesAPI
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

    def get_translation(self, code_text):
        """
        The function get text from web client and returns list of translated words
        :param code_text : text
        :returns translated_list : list
        """
        logging.info("Got request from client " + code_text)
        translated_list = []
        p = Parser(self.language)
        keywords_list = p.parse_text(code_text)
        for word in keywords_list:
            logging.info("in keywords")
            try:
                logging.info("Found in DB")
                translated_list.append(DAL.get_data_from_db(word, self.language))
            except DataNotExistException:
                logging.info("Not found in DB")
                word_type = p.get_word_type(word)
                translated_list.append(self.add_keyword(word, word_type))
        return translated_list

    def add_keyword(self, keyword, word_type):
        """
        This functions add new keywords to DB, after searching in google
        :param keyword: string
        :param word_type: string
        """
        url = self.google_search(keyword)
        logging.info("URL" + url)
        la = LanguagesAPI()
        result, code = la.http_request_using_urlfetch(http_url=url)
        rp = ResultParser(self.language)
        translation = rp.find_by_id(result)
        if not translation:
            translation = rp.strip_text_from_html(result)

        try:
            data = DAL.save_data_in_db(self.language, keyword, word_type, url, translation, approved=False)
            logging.info("Saving in DB new translation")
            return data
        except DataExistException:
            logging.info("Data already saved in db")

    def google_search(self, keyword):
        """
        Search in google for keyword, returns url of website with answer.
        Get few results from google - if one of the results is default - return it,
        if not - return the first result
        :param keyword: string
        :return: url
        :rtype : string
        """
        s = self.language + " " + keyword + " site:" + default_urls[self.language]
        g = pygoogle(s)
        g.pages = 1
        urls = g.get_urls()
        print urls

        for url in urls:
            if url in default_urls[self.language]:
                return url
        return urls[0]

