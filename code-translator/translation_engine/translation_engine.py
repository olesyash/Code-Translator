__author__ = 'olesya'
from parser import Parser
from DAL import *
import logging
from lib.googleapiclient.discovery import build
from engine.result_parser import *
from engine.languages_API import *
from lib.googleapiclient.http import HttpError


'''
Getting code from web side and using 3 steps before giving result back to web side
1. Use Parser to isolate which words should be "translated"
2. Use specific language api treatment to access needed API
3. Use specific language result parser to get the right result
'''


class TranslationEngine():
    def __init__(self, language):
        self.language = language
        self.res_parser = ResultParser(self.language)
        self.parser_obj = Parser(self.language)
        self.la = LanguagesAPI()
        self.url = ""
        self.MAX_RESULTS = 30
        self.possible_urls = []
        self.rp = ResultParser(self.language)
        self.function_mapper = {"id": self.rp.find_by_id,
                                "class": self.rp.find_by_class,
                                "clear": self.res_parser.strip_text_from_html,
                                "all": lambda html: html}

    def get_translation(self, code_text):
        """
        The function get text from web client and returns list of dictionaries describing translated words
        :param code_text : text
        :returns translated_list : list
        """
        logging.info("Got request from client: " + code_text)
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
        if not url:
            return None

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
        _type, name = get_details_about_url(self.url)
        func = self.function_mapper.get(_type)
        logging.info("parsing using " + str(func))
        if name:
            translation = func(result, name)
        else:
            translation = func(result)
        logging.debug("Translation " + translation)
        return translation

    def classify_keywords(self, keyword, word_type):
        if word_type == KEYWORD:
            # if keyword_is_title(self.language, keyword, "statements"):
            #     return STATEMENT
            # elif keyword_is_title(self.language, keyword, "data_types"):
            #     return DATA_TYPE
            # elif keyword_is_title(self.language, keyword, "expressions"):
            #     return EXPRESSION
            # elif keyword_is_title(self.language, keyword, "operators"):
            #     return OPERATOR
            return get_keyword_classification(self.language, keyword)

            # res = keyword_in_other(self.language, keyword)
            # if res:
            #     return res
            # return KEYWORD
        else:
            return word_type

    def url_search(self, keyword, word_type):
        """
        Search in google for keyword, returns first url of approved website,
        Try max 30 google search results
        :param keyword: string
        :return: url
        :rtype : string
        """
        counter = 1
        # Classify keyword to get better search accuracy
        word_type = self.classify_keywords(keyword, word_type)

        # Get approved urls list depending on language
        language_url_list = get_urls_for_language(self.language)
        search_string = self.language + " " + keyword + " " + word_type

        self.url = None
        while counter < self.MAX_RESULTS:
            logging.info("search in google: " + search_string)
            logging.info("counter " + str(counter))
            urls = self.custom_google_search(search_string, counter)
            if not urls:
                return []
            if not self.url:
                self.url = urls[0]  # Save default url to be the first one
            for url in urls:
                for i in language_url_list:
                    if i in url and "pdf" not in url:
                        self.url = url
                        return url
            counter += 10
            return self.url

    def custom_google_search(self, search_string, index=1):
        keys = ["AIzaSyDM_PtVl-yhPmhgft6Si02vMJmOCatFK_w", "AIzaSyD9ufY0LcUPB8UO4RA4FVB8rJdZC12pKKc"]
        _id = "000167123881013238899:uys_fzjgaby"
        for i in range(0, 2):
            try:
                service = build("customsearch", "v1",
                                developerKey=keys[i])
                res_json = service.cse().list(
                    q=search_string,
                    cx=_id,
                    start=index
                ).execute()
                break
            except HttpError:
                continue
        else:
            logging.error("Quota ended")
            return []

        urls = []
        logging.info("custom google search result: " + str(res_json))
        try:
            for i in res_json['items']:
                urls.append(i['link'])
            logging.info("Urls: {urls}".format(urls=str(urls)))
            return urls
        except KeyError:
            return []

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
        # run on list of tuples, each element is a tuple
        for element in parsed_list:
            word_type = element[0]  # word type
            word = element[1]  # word
            line = element[2][1]  # line number
            if cur_line != line:  # if not first line, update shift to 0
                cur_line = line
                shift = 0
            char_place = element[2][2] + shift  # location of word + shift
            print "char place " + str(char_place)
            text = lines[line-1]  # take original text on the line of parsed list
            print "text before if: " + text  # text before manipulation
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
