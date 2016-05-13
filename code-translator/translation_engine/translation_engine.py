__author__ = 'olesya'
from my_parser import Parser
from DAL import *
import logging
from apiclient.discovery import build
from lib.pygoogle import pygoogle
from languages_specific_features import *
from engine.result_parser import *
from engine.languages_API import *

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
        self.la = LanguagesAPI()

    def get_translation(self, code_text):
        """
        The function get text from web client and returns list of dictionaries describing translated words
        :param code_text : text
        :returns translated_list : list
        """
        logging.info("Got request from client " + code_text)
        translated_list = []
        keywords_list, parsed = self.parser_obj.run_parser(code_text)
        final_code_text = self.reformat_parsed_text(code_text, parsed)
        for word, word_type in keywords_list.iteritems():
            logging.info("in keywords, the word is: " + word)
            try:
                logging.info("Found in DB")
                translated_list.append(DAL.get_data_from_db(word, self.language))
            except DataNotExistException:
                logging.info("Not found in DB")
                res = self.add_keyword(word, word_type)
                if res:
                    translated_list.append(res)
                else:
                    translated_list.append(self.prepare_mock_answer(word, word_type, self.language))
        return translated_list, final_code_text

    def prepare_mock_answer(self, keyword, word_type, language):
        data = dict()
        data['language'] = language
        data['keyword'] = keyword
        data['type'] = word_type
        data['link'] = ""
        data['translation'] = "It's probably user's function definition"
        data['approved'] = False
        return data

    def add_keyword(self, keyword, word_type):
        """
        This functions add new keywords to DB, after searching in google
        :param keyword: string
        :param word_type: string
        """
        url = self.google_search(keyword, word_type)
        logging.info("URL" + str(url))

        try:
            result, code = self.la.http_request_using_urlfetch(http_url=url)
        except WrongURL:
            url = self.google_search(keyword, word_type, site=False)
            try:
                result, code = self.la.http_request_using_urlfetch(http_url=url)
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

    def classify_keywords(self, keyword, word_type):
        if word_type == KEYWORD and keyword in languages_statements[self.language]:
            return STATEMENT
        return KEYWORD

    def google_search(self, keyword, word_type, site=True):
        """
        Search in google for keyword, returns first url of website with answer.
        Search in google using "site:" option, making google to search in specific site
        :param keyword: string
        :return: url
        :rtype : string
        """
        key = "AIzaSyDM_PtVl-yhPmhgft6Si02vMJmOCatFK_w"
        _id = "000167123881013238899:uys_fzjgaby"

        word_type = self.classify_keywords(keyword, word_type)
        if site:
            search_string = self.language + " " + keyword + " " + word_type + " site:" + default_urls[self.language]
        else:
            search_string = self.language + " " + keyword + " " + word_type
        logging.info("search in google: " + search_string)
        service = build("customsearch", "v1",
                        developerKey=key)
        res_json = service.cse().list(
            q=search_string,
            cx=_id,
        ).execute()
        urls = []
        for i in res_json['items']:
            urls.append(i['link'])
        logging.info("Urls: {urls}".format(urls=str(urls)))
        for url in urls:
            if "pdf" not in url:
                return url

    def reformat_parsed_text(self, code_text, parsed_list):
        """
        This function get parsed object and creating new text with suitable tags
        parsed list is a list of tuples, each tuple has (type, word, ('', line, location))
        :param code_text: string (original code text)
        :param parsed_list: list of tuples (parsed object)
        :return: formatted code text with tags
        :rtype string
        """
        lines = code_text.split('\n')
        cur_line = 1
        shift = 0
        for element in parsed_list:
            word_type = element[0]
            word = element[1]
            line = element[2][1]
            if cur_line != line:
                cur_line = line
                shift = 0
            char_place = element[2][2] + shift
            print "char place " + str(char_place)
            text = lines[line-1]
            print "text before if: " + text
            print word
            print text[char_place:char_place+len(word)]
            print(text[char_place:char_place+len(word)] == word)
            if text[char_place:char_place+len(word)] == word:
                print "in if"
                text = text[:char_place] + self.add_tag(word_type, word) + text[char_place+len(word):]
                shift += 22 + len(word_type)
                print "shift " + str(shift)
                print "text " + text
                lines[line-1] = text
        final_code_text = '\n'.join(lines)
        print "final code: " + final_code_text
        return final_code_text

    def add_tag(self, _type, word):
        """
        This function add html tag for word to describe it's type
        :param _type: string - type of word
        :param word: string - the word need translation
        :return: the word with suitable tag describing the type
        """
        return '<span class="' + _type + '">' + word + '</span>'
