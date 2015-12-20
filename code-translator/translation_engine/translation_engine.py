__author__ = 'olesya'
from parser import Parser
from DAL import *
import  logging

class TranslationEngine():

    @staticmethod
    def get_translation(code_text, language):
        logging.info("Getted request from client " + code_text)
        translated_list = []
        keywords_list = Parser.parse_text(code_text)
        for word in keywords_list:
            logging.info("in keywords")
            try:
                logging.info("Found in DB")
                translated_list.append(DAL.get_data_from_db(word, language))
            except DataNotExistException:
                logging.info("Not found in DB")

        return translated_list





