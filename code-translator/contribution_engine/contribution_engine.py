__author__ = 'olesya'
from DAL import *
from engine.result_parser import *
from engine.languages_API import *
import logging

class ContributionEngine():
    def __init__(self, language, keyword):
        self.THANKS_BUT_NO_THANKS = "Thank you, but the keyword already translated"
        self.THANKS_FOR_APPROVE = "Thank you for keyword approve"
        self.THANKS_FOR_CONTRIBUTION = "Thank you for your contribution!"
        self.GET_CONTRIBUTION = "Please insert contribution details: "
        self.WRONG_URL = "We could not use this URL. Please recheck spelling"
        self.WRONG_TRANSLATION = "Are you sure this link describing the keyword?"
        self.language = language
        self.keyword = keyword
        self.dal = DAL()
        self.res_parser = ResultParser(self.language)

    def contribute(self):
        res = self.check_keyword_exist()
        if not res:
            return self.get_contribution()
        else:
            if self.check_keyword_approved(res):
                return self.THANKS_BUT_NO_THANKS
            else:
                return self.show_existing_translation(res)

    def user_approve(self, approve):
        if approve:
            self.set_approved(True)
            return self.THANKS_FOR_APPROVE
        else:
            self.get_contribution()

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
        return self.GET_CONTRIBUTION

    def show_existing_translation(self, res):
        return res['translation']

    def set_approved(self, approved):
        self.dal.set_approved(self.keyword, self.language, approved)

    def run_check_on_contribution(self, translation):
        res = self.res_parser.strip_text_from_html(translation)
        return self.res_parser.find_needed_info(res, self.keyword)

    def get_translation_by_id(self, word_type, link, html_id):
        la = LanguagesAPI()
        try:
            result, code = la.http_request_using_urlfetch(http_url=link)
        except WrongURL:
            return self.WRONG_URL
        translation = self.res_parser.find_by_id(result, html_id)

        if not self.run_check_on_contribution(translation):
            return self.WRONG_TRANSLATION

        # TODO: check user's level, if admin save in DB, if not save in contribution db
        try:
            DAL.save_data_in_db(self.language, self.keyword, word_type, link, translation, approved=True)
            logging.info("Saving in DB new contributed translation")
            return self.THANKS_FOR_CONTRIBUTION
        except DataExistException:
            logging.info("Data already saved in db")






