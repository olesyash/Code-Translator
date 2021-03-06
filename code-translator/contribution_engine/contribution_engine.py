__author__ = 'olesya'
from DAL import *
from engine.result_parser import *
from engine.languages_API import *
from translation_engine.languages_specific_features import LanguagesSpecificFeatures
import logging

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class ContributionEngine():
    def __init__(self, language, keyword=None):
        self.THANKS_BUT_NO_THANKS = "Thank you, but the keyword already translated"
        self.THANKS_FOR_APPROVE = "Thank you for the keyword approve!"
        self.THANKS_FOR_CONTRIBUTION = "Thank you for your contribution!"
        self.GET_CONTRIBUTION = "Please insert contribution details: "
        self.WRONG_URL = "We could not use this URL. Please recheck spelling"
        self.WRONG_TRANSLATION = "Are you sure this link describing the keyword?"
        self.WRONG_WORD_TYPE = "Please recheck keyword type, it could not be keyword"
        self.ERROR_CODE = -1
        self.OK_CODE = 0
        self.language = language
        self.keyword = keyword
        self.dal = DAL()
        self.res_parser = ResultParser(self.language)
        self.function_mapper = {"id": self.res_parser.find_by_id,
                                "class": self.res_parser.find_by_class,
                                "p": self.res_parser.find_by_p,
                                "clear": self.res_parser.strip_text_from_html,
                                "nothing": lambda html: html}

    def contribute(self):
        """
        Contribution act on keyword:
         if exist in DB and approved - say thank you
         if exist in DB and not approved - ask for approval
         if do not exist in DB - ask for contribution
        :return: String describing the next step
        """
        logging.info("Got keyword: {}, language: {}".format(self.keyword, self.language))
        res = self.check_keyword_exist()
        if not res:
            return self.get_contribution()
        else:
            if self.check_keyword_approved(res):
                return self.THANKS_BUT_NO_THANKS
            else:
                return self.show_existing_translation(res)

    def user_approve(self):
        """
        If contributor approved keyword, send thank you,
        else ask for new contribution
        """
        self.set_approved(True)
        return self.THANKS_FOR_APPROVE

    def check_keyword_exist(self):
        """
        Check if keyword exist in DB
        :return: dictionary with keyword details, or empty dictionary if not exist
        """
        try:
            return self.dal.get_data_from_db(self.keyword, self.language)
        except DataNotExistException:
            return []

    def check_keyword_approved(self, res):
        """
        Get dictionary describing the keyword and return if keyword approved
        :param res: dictionary
        :rtype boolean
        :return:
        """
        return eval(res['approved']) if res else False

    def get_contribution(self):
        """
        Return final String asking to contribute
        :return:
        """
        return self.GET_CONTRIBUTION

    def show_existing_translation(self, res):
        """
        Return existing translation of saved keyword in DB
        :param res: Dictionary of keyword saved in DB
        :return: String - the transaltion
        """
        return res['translation']

    def set_approved(self, approved):
        """
        Change entry in DB of approved
        :param approved: new value to set to
        """
        self.dal.set_approved(self.keyword, self.language, approved)

    def run_check_on_contribution(self, translation):
        """
        Check if the text describing the keyword
        :param translation: String that supposed to describe the keyword
        :rtype Boolean
        :return: Is the text describing the keyword
        """
        res = self.res_parser.strip_text_from_html(translation)
        return self.res_parser.find_needed_info(res, self.keyword)

    def check_is_keyword(self):
        """
        This function check if it is really defined keyword in language
        :return:
        """
        lsf = LanguagesSpecificFeatures(self.language)
        list_of_keywords = lsf.find_all_keywords()
        if not list_of_keywords:
            return False
        return self.keyword in list_of_keywords

    def get_translation(self, link, translation_type, name=None, word_type=None):
        """
        This function get information from contributor:
        which url to access
        which element to look for with the given name
        Using this rules executing the relevant function on html to get the needed translation.
        If translation pass the check, add it to DB
        :param word_type: keyword type (keyword, function .... )
        :param link: url to try to get info from
        :param translation_type: which function to call
        :param name: the name of element e.g id=name
        :return: return thankful message with new translation or error
        """
        if word_type == "keyword":
            logging.info("marked as keyword")
            res = self.check_is_keyword()
            if not res:
                return self.WRONG_WORD_TYPE, self.ERROR_CODE

        la = LanguagesAPI()
        try:
            result, code = la.http_request_using_urlfetch(http_url=link)
        except WrongURL:
            return self.WRONG_URL, self.ERROR_CODE

        func = self.function_mapper.get(translation_type)
        if name:
            translation = func(result, name)
        else:
            translation = func(result)
        logging.info("Translation is {}".format(translation))

        if not self.run_check_on_contribution(translation):
            return self.WRONG_TRANSLATION, self.ERROR_CODE

        return translation, self.OK_CODE

    def save_in_db(self, word_type, link, translation):
        try:
            DAL.save_data_in_db(self.language, self.keyword, word_type, link, translation, approved=True)
            logging.info("Saving in DB new contributed translation")
        except DataExistException:
            logging.info("Updating data in DB")
            DAL.update_data_in_db(self.language, self.keyword, word_type, link, translation)
        return self.THANKS_FOR_CONTRIBUTION

    def add_new_language_json(self, data):
        """
        This function get all parsing data of a new language in dictionary and saves it in DB
        :param data: dictionary
        :return: True if all saved, False if there were errors in saving
        """
        dal = DAL()
        try:
            dal.save_language_data(self.language, data)
            return True
        except Exception as e:
            logging.error(e.message)
            return False

    def add_urls_for_language(self, data):
        """
        Save in DB all data about languages urls
        :param data: dictionary
        :return: True if all saved, False if there were errors in saving
        """
        try:
            self.dal.save_language_details(self.language, "urls", data["urls"])
            for url in data["urls"]:
                self.dal.set_url_details(url, data[url]['type'], data[url]['name'])
            self.dal.add_language(self.language)
            return True
        except Exception as e:
            logging.error(e)
            return False

    def add_classification_for_language(self, data):
        """
        Save in DB classification data for new language
        :param data: dictionary
        :return: True if all saved, False if there were errors in saving
        """
        try:
            self.dal.save_classification(self.language, "statement", data["statements"])
            self.dal.save_classification(self.language, "data type", data["data_types"])
            self.dal.save_classification(self.language, "expression", data["expressions"])
            self.dal.save_classification(self.language, "operator", data["operators"])
            other_list = data['other']
            if other_list:
                for key, value in other_list.iteritems():
                    self.dal.save_classification(self.language, key, value)
            return True
        except Exception as e:
            logging.info(20*"*")
            logging.info(e.message)
            logging.info(e)
            return False









