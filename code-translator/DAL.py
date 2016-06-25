__author__ = 'olesya'

from models.models import *
import datetime
import logging


class DAL():
    # ----------------------------
    #  User treatment functions
    # ----------------------------

    def __init__(self):
        pass

    @staticmethod
    def add_new_user(firstname, lastname, nickname, password, email, user_role):
        """
        This functions get user details and saves new user in DB.
        Throwing UserExistException if user with same email already exist
        :param firstname:
        :param lastname:
        :param nickname:
        :param password:
        :param email:
        :param user_role:
        :except: UserExistException
        """
        if Users.find_user_by_email(email):
            raise UserExistException()
        else:
            _newUser = Users()
            _newUser.first_name = firstname
            _newUser.last_name = lastname
            _newUser.nickname = nickname
            _newUser.password = password
            _newUser.email = email
            _newUser.user_role = user_role
            _newUser.put()

    @staticmethod
    def get_user_level(email):
        """
        This function get user's email and return his level
        Throws UserNotExistException if no user with such email
        :returns user_role
        :rtype string
        :except UserNotExistException
        """
        _qry = Users.find_user_by_email(email)
        if _qry:
            return _qry.user_role
        else:
            raise UserNotExistException()


    @staticmethod
    def set_user_level(email, role):
        """
        This function get user's email and role and update his role
        :param email:
        :param role:
        :except UserNotExistException
        """
        _qry = Users.find_user_by_email(email)
        if _qry:
            _qry.user_role = role
            _qry.put()
        else:
            raise UserNotExistException()

    @staticmethod
    def check_user_passwd(email, passwd):
        """
        This function get email and password of an user and checks if password is correct
        :param email: string
        :param passwd: string
        :return: true if password is correct
        :rtype: boolean
        """
        _qry = Users.find_user_by_email(email)
        if _qry:
            if _qry.password == passwd:
                return _qry.nickname
            else:
                return False
        else:
            raise UserNotExistException()

    # ----------------------------
    #  Data treatment functions
    # ----------------------------


    @staticmethod
    def save_data_in_db(language, keyword, word_type, link, translation, approved):
        """
        This function save new data to DB
        :param language: string
        :param keyword: string
        :param word_type: string
        :param link: string
        :param translation: text
        :param approved: boolean
        :except DataExistException
        """
        res = LanguagesData.find_keyword(keyword, language)
        if not res:
            _newData = LanguagesData()
            _newData.language = language
            _newData.keyword = keyword
            _newData.type = word_type
            _newData.link = link
            _newData.translation = translation
            _newData.approved = approved
            _newData.put()
            return create_dict(language, keyword, word_type, link, translation, approved)
        else:
            raise DataExistException()

    @staticmethod
    def update_data_in_db(language, keyword, word_type, link, translation):
        """
        This function save new data to DB
        :param language: string
        :param keyword: string
        :param word_type: string
        :param link: string
        :param translation: text
        :param approved: boolean
        :except DataExistException
        """
        res = LanguagesData.find_keyword(keyword, language)
        if res:
            res.language = language
            res.keyword = keyword
            res.type = word_type
            res.link = link
            res.translation = translation
            res.approved = True
            res.put()
        else:
            raise DataNotExistException()

    @staticmethod
    def get_data_from_db(keyword, language):
        """
        This function getting data from DB for specific keyword
        :param keyword : string
        :except DataNotExistException
        :returns data
        :rtype json
        """
        res = LanguagesData.find_keyword(keyword, language)
        if res:
            return create_dict(res.language, res.keyword, res.type, res.link, res.translation, str(res.approved))
        else:
            raise DataNotExistException

    @staticmethod
    def set_approved(keyword, language, approved):
        """
        This function get keyword, language, approved and set approved to be approved
        :param email:
        :param role:
        :except DataNotExistException
        """
        _qry = LanguagesData.find_keyword(keyword, language)
        if _qry:
            _qry.approved = approved
            _qry.put()
        else:
            raise DataNotExistException()

    @staticmethod
    def save_language_details(language, title, keywords_list):
        """
        This function get language, list of keywords and a title for the list and saves it in DB
        :param language
        :param title
        :param keywords_list
        """
        _newData = LanguagesParsingData()
        if not LanguagesParsingData.find_language_by_type(language, title):
            _newData.language = language
            _newData.list_of_keywords = keywords_list
            _newData.type = title
            _newData.put()

    @staticmethod
    def get_language_details(language, _type=None):
        """
        This function get language and return all associated information in DB for this language
        :param language:
        :return: dictionary of all data
        """
        logging.info("in get languages details, type {} time {} ".format(_type, str(datetime.datetime.now())))
        _newData = LanguagesParsingData()

        if _type:
            qrys = _newData.find_language_by_type(language, _type)
        else:
            qrys = _newData.find_language(language)
        all_data = {}

        if not qrys:
            return []
        dict_of_others = {}
        for q in qrys:
            if _type:
                return q.list_of_keywords
            all_data["language"] = q.language
            string_of_keywords = q.list_of_keywords
            print string_of_keywords
            dict_of_others[q.type] = string_of_keywords
        all_data["others"] = dict_of_others
        print all_data
        return all_data

    @staticmethod
    def set_url_details(url, _type, name):
        """
        This function save url details in DB only if not already exist
        :param url: string
        :param _type: string
        :param name: string
        :return:
        """
        _newData = LanguagesUrlsData()
        res = _newData.find_url(url)
        if not res:
            _newData.url = url
            _newData.type = _type
            _newData.name = name
            _newData.put()

    @staticmethod
    def get_url_details(url):
        """
        This function get url and return information about it from DB
        :param url: the url that information needed about
        :return: dictionary of all data
        """
        _newData = LanguagesUrlsData()
        qry = _newData.find_url(url)
        if qry:
            return qry.type, qry.name
        else:
            return "all", ""

    def add_language(self, language):
        new = AllLanguages()
        res = self.get_all_languages()
        if not res:
            if not isinstance(language, basestring):
                new.languages = language
            else:
                new.languages = [language]
            new.put()
            return True

        if language in res:
            return False
        else:
            res.append(language)
            _qry = AllLanguages.query().get()
            _qry.languages = res
            _qry.put()
            return True

    def get_all_languages(self):
        _qry = AllLanguages.query()
        q = _qry.get()
        print q
        if q:
            print "q.languages" + str(q.languages)
            return q.languages
        else:
            return []

    @staticmethod
    def save_classification(language, _type, list_of_keywords):
        for keyword in list_of_keywords:
            res = DAL.get_classification(language, keyword)
            if res != "keyword":
                continue
            new_element = LanguagesClassificationData()
            new_element.language = language
            new_element.keyword = keyword
            new_element.type = _type
            new_element.put()


    @staticmethod
    def get_classification(language, keyword):
        res = LanguagesClassificationData.find_keyword_classification(language, keyword)
        return res.type if res else "keyword"

    def save_language_data(self, language, data):
        new = ParsingData()
        new.language = language
        new.data = data
        new.put()

    def get_all_data_for_language(self, language):
        qry = ParsingData.query(ParsingData.language == language).get()
        if qry:
            return qry.data
        # print qry.to_dict()
        #return qry.to_dict()


def create_dict(language, keyword, type, link, translation, approved):
    """
    This function gets info and put it in dictionary
     :returns dictionary with all data
     :rtype dictionary
    """
    data = dict()
    data['language'] = language
    data['keyword'] = keyword
    data['type'] = type
    data['link'] = link
    data['translation'] = translation
    data['approved'] = str(approved)
    return data


class UserExistException(Exception):
    def __init__(self):
        self.message = "User with this mail already exist!"


class UserNotExistException(Exception):
    def __init__(self):
        self.message = "User with this mail doesn't exist!"


class DataExistException(Exception):
    def __init__(self):
        self.message = "Data for this keyword already exist!"


class DataNotExistException(Exception):
    def __init__(self):
        self.message = "Data for this keyword not exist!"