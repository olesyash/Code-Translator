__author__ = 'olesya'

from models.models import *
import json


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
                return True
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
        :except UserNotExistException
        """
        _qry = LanguagesData.find_keyword(keyword, language)
        if _qry:
            _qry.approved = approved
            _qry.put()
        else:
            raise UserNotExistException()


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
        self.message = "Data for this key word already exist!"


class DataNotExistException(Exception):
    def __init__(self):
        self.message = "Data for this key word not exist!"