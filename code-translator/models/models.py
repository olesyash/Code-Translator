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
    def find_keyword(word, language):
        """
        This function find data in DB by keyword and language
        :param word, language:
        :return: LanguagesData Object if found in DB, false if not
        """
        _qry = LanguagesData.query()

        _q = _qry.filter(LanguagesData.language == language)
        _q = _q.filter(LanguagesData.keyword == word)
        q = _q.get()
        if q:
            return q
        else:
            return False
