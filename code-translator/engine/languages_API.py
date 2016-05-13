__author__ = 'olesya'

from google.appengine.api import urlfetch


class LanguagesAPI():

    def http_request_using_urlfetch(self, http_url, params=None):
        """
        This function make http request to given url with given params using url fetch library
        :param http_url: string
        :param params: list
        :return: content, status code
        :except WrongURL exception
        """
        if http_url == None:
            raise WrongURL
        if params is not None:
            url = self.prepare_get_url(http_url, params)
        else:
            url = http_url
        try:
            result = urlfetch.fetch(url=url, deadline=30)
            return result.content, result.status_code
        except:
            raise WrongURL

    def prepare_get_url(self, url, params):
        """
        This function prepare url by parameters to the url
        :param url: string
        :param params: list
        :return url
        :rtype string
        """
        new_url = url
        if params is not None:
            for key, value in params.iteritems():
                new_url = new_url + key + '=' + str(value)
                if key != params.keys()[-1]:
                    new_url += "&"
        return new_url


class WrongURL(Exception):
    def __init__(self):
        self.message = "The url is wrong"