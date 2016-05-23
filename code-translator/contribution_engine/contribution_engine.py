__author__ = 'olesya'
from DAL import *
from engine.result_parser import *
from engine.languages_API import *
import logging

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class ContributionEngine():
    def __init__(self, language, keyword):
        self.THANKS_BUT_NO_THANKS = "Thank you, but the keyword already translated"
        self.THANKS_FOR_APPROVE = "Thank you for the keyword approve!"
        self.THANKS_FOR_CONTRIBUTION = "Thank you for your contribution!"
        self.GET_CONTRIBUTION = "Please insert contribution details: "
        self.WRONG_URL = "We could not use this URL. Please recheck spelling"
        self.WRONG_TRANSLATION = "Are you sure this link describing the keyword?"
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
        If contributor approved keyword, send thanks you,
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

    def get_translation(self, word_type, link, translation_type, name=None):
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
        # TODO: check user's level, if admin save in DB, if not save in contribution db
        try:
            DAL.save_data_in_db(self.language, self.keyword, word_type, link, translation, approved=True)
            logging.info("Saving in DB new contributed translation")
        except DataExistException:
            logging.info("Updating data in DB")
            DAL.update_data_in_db(self.language, self.keyword, word_type, link, translation)
        return self.THANKS_FOR_CONTRIBUTION









