__author__ = 'olesya'

from HTMLParser import HTMLParser
from lib.bs4 import BeautifulSoup

possible_id = {
    "Python": 'content',
    "Java": 'PageContent'
}


class ResultParser():
    def __init__(self, language):
        self.language = language

    def find_by_default_id(self, html_data):
        """
        This function get html text and return the content of specific class id that is defined for each language
        :param html_data: html string
        :return: string of the content by id or empty string if id not found in the html
        """
        soup = BeautifulSoup(html_data, 'html.parser')
        id_text = possible_id[self.language]

        found_needed_data = soup.find(id=id_text)
        try:
            str(found_needed_data)
        except RuntimeError as e:
            found_needed_data = None
        print(found_needed_data)
        if found_needed_data is not None:
            return str(found_needed_data)
        else:
            return ""

    def find_by_id(self, html_data, given_id):
        """
        This function get html text and return the content of specific class id that is given as paramrter
        :param html_data: html string
        :param given_id: string
        :return: string of the content by id or empty string if id not found in the html
        """
        soup = BeautifulSoup(html_data, 'html.parser')
        found_needed_data = soup.find(id=given_id)
        print(found_needed_data)
        if found_needed_data is not None:
            return str(found_needed_data)
        else:
            return ""

    def find_by_p(self, html_data):
        """
        This function get html text and return the content of class p
        :param html_data:  html string
        :return: string of the content by p or empty string if p not found in the html
        """
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
        """
        The function get html text and return clean text without html tags
        :param html_text: html string
        :return:
        """
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