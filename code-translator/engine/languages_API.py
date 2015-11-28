__author__ = 'olesya'

from google.appengine.api import urlfetch


class LanguagesAPI():

    def http_request_using_urlfetch(self, http_url, params):
        url = self.prepare_get_url(http_url, params)
        result = urlfetch.fetch(url=url,
                                deadline=30)
        return result.content, result.status_code

    def prepare_get_url(self, url, params):
        new_url = url
        if params is not None:
            for key, value in params.iteritems():
                new_url = new_url + key + '=' + str(value)
                if key != params.keys()[-1]:
                    new_url += "&"
        return new_url