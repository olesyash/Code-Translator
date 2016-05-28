__author__ = 'olesya'
from my_parser import Parser
from DAL import *
import logging
from lib.googleapiclient.discovery import build
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
        self.url = ""
        self.rp = ResultParser(self.language)
        self.function_mapper = {"id": self.rp.find_by_id,
                                "class": self.rp.find_by_class,
                                "all": lambda html, _: html}

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
        url = self.url_search(keyword, word_type)
        logging.info("URL: " + str(url))

        try:
            result, code = self.la.http_request_using_urlfetch(http_url=url)
        except WrongURL:
            result = None

        if result is not None:
            translation = self.parse_result(result)
            if translation == "":
                logging.info("Could not parse the result")
                new_url = self.rp.try_frame(result)
                self.url += new_url
                try:
                    result, code = self.la.http_request_using_urlfetch(http_url=self.url)
                    translation = self.parse_result(result)
                    if translation == "":
                        translation = result
                except WrongURL:
                    return result

            try:
                data = DAL.save_data_in_db(self.language, keyword, word_type, url, translation, approved=False)
                logging.info("Saving in DB new translation")
                return data
            except DataExistException:
                logging.info("Data already saved in db")
        else:
            return None

    def parse_result(self, result):
        _type = ""
        name = ""
        for key in url_info:
            if key in self.url:
                _type, name = url_info[key].items()[0]
                break

        func = self.function_mapper.get(_type)
        logging.info("parsing using " + str(func))
        translation = func(result, name)
        logging.debug("Translation " + translation)
        return translation

    def classify_keywords(self, keyword, word_type):
        if word_type == KEYWORD:
            if keyword in languages_statements[self.language]:
                return STATEMENT
            elif keyword in languages_data_types[self.language]:
                return DATA_TYPE
            elif keyword in languages_expressions[self.language]:
                return EXPRESSION
            elif keyword in languages_operators[self.language]:
                return OPERATOR
            return KEYWORD
        else:
            return word_type

    def url_search(self, keyword, word_type):
        """
        Search in google for keyword, returns first url of website with answer.
        Search in google using "site:" option, making google to search in specific site
        :param keyword: string
        :return: url
        :rtype : string
        """
        counter = 1
        word_type = self.classify_keywords(keyword, word_type)

        language_url_list = default_urls[self.language]
        search_string = self.language + " " + keyword + " " + word_type

        while counter < 30:
            logging.info("search in google: " + search_string)
            logging.info("counter " + str(counter))
            urls = self.custom_google_search(search_string, counter)

            for i in language_url_list:
                for url in urls:
                    if i in url and "pdf" not in url:
                        self.url = url
                        return url
            counter += 10

    def custom_google_search(self, search_string, index=1):
        #key = "AIzaSyDM_PtVl-yhPmhgft6Si02vMJmOCatFK_w"
        key = "AIzaSyD9ufY0LcUPB8UO4RA4FVB8rJdZC12pKKc"
        _id = "000167123881013238899:uys_fzjgaby"
        service = build("customsearch", "v1",
                        developerKey=key)
        res_json = service.cse().list(
            q=search_string,
            cx=_id,
            start=index
        ).execute()
        urls = []
        for i in res_json['items']:
            urls.append(i['link'])
        logging.info("Urls: {urls}".format(urls=str(urls)))
        return urls

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
