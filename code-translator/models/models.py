__author__ = 'olesya'

from google.appengine.ext import ndb


class Users(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    nickname = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
    user_role = ndb.StringProperty()

    @staticmethod
    def find_user_by_email(email):
        """
        This function find user in DB by his mail
        :param email:
        :return: users object if found in DB, false if not
        """
        _qry = Users.query(Users.email == email).get()
        if _qry:
            return _qry
        else:
            return False


class LanguagesData(ndb.Model):
    language = ndb.StringProperty()
    keyword = ndb.StringProperty()
    type = ndb.StringProperty()
    link = ndb.StringProperty()
    translation = ndb.TextProperty()
    approved = ndb.BooleanProperty()

    @staticmethod
    def find_keyword(word, language):
        """
        This function find data in DB by keyword and language
        :param word, language:
        :return: LanguagesData Object if found in DB, false if not
        """
        _qry = LanguagesData.query(LanguagesData.language == language, LanguagesData.keyword == word)
        q = _qry.get()
        if q:
            return q
        else:
            return False


class LanguagesParsingData(ndb.Model):
    language = ndb.StringProperty()
    list_of_keywords = ndb.TextProperty(repeated=True)
    type = ndb.StringProperty()


    @staticmethod
    def find_language(language):
        """
        This function find all data inlanguages parsing data by language
        :param word, language:
        :return: list of LanguagesParsingData Objects if found in DB, false if not
        """
        q = LanguagesParsingData.query(LanguagesParsingData.language == language)
        if q:
            return q
        else:
            return False

    @staticmethod
    def find_language_by_type(language, _type):
        """
        This function find data in DB by type and language
        :param word, language:
        :return: list of LanguagesParsingData Objects if found in DB, false if not
        """
        qrys  = LanguagesParsingData.query(LanguagesParsingData.language == language, LanguagesParsingData.type == _type)
        q = qrys.get()
        if q:
            return qrys
        else:
            return False


class LanguagesUrlsData(ndb.Model):
    url = ndb.StringProperty()
    type = ndb.StringProperty()
    name = ndb.StringProperty()

    @staticmethod
    def find_url(url):
        """
        This function find all info about url
        :param url: string
        :return: The relevant data about url from db
        """
        _qry = LanguagesUrlsData.query(url <= LanguagesUrlsData.url)
        q = _qry.get()
        if q:
            return q
        else:
            return False


class AllLanguages(ndb.Model):
    languages = ndb.StringProperty(repeated=True)