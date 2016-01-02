__author__ = 'olesya'

from HTMLParser import HTMLParser
from lib.bs4 import BeautifulSoup

possible_id = {
    "Python":'content',
    "Java": 'PageContent'
}


class ResultParser():
    def __init__(self, language):
        self.language = language

    def find_by_id(self, html_data):
        soup = BeautifulSoup(html_data, 'html.parser')
        id_text = possible_id[self.language]
        found_needed_data = soup.find(id=id_text)
        print(found_needed_data)
        if found_needed_data is not None:
            return str(found_needed_data)
        else:
            return ""

    def find_by_p(self, html_data):
        soup = BeautifulSoup(html_data, 'html.parser')
        found_needed_data = soup.p
        if found_needed_data is not None:
            try:
                return found_needed_data.get_text()
            except AttributeError:
                return found_needed_data
        else:
            return ""

    def strip_text_from_html(self, html_text):
        return strip_tags(html_text)

    def find_needed_info(self, plain_text, needed_info):
        if needed_info in plain_text:
            return True


'''
HTML parser
'''


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()