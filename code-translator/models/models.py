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

    @staticmethod
    def find_keyword(word):
        """
        This function find data in DB by keyword
        :param word:
        :return: LanguagesData Object if found in DB, false if not
        """
        _qry = LanguagesData.query(LanguagesData.keyword == word).get()
        if _qry:
            return _qry
        else:
            return False