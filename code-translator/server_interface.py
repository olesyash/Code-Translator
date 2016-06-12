#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This Class will perform the connection between web to server.
"""

import webapp2
import jinja2
from translation_engine.translation_engine import *
from contribution_engine.contribution_engine import *
import logging
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader("web"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("Main handler: loading landing page")
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class ContributionHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('contribution_page.html')
        self.response.write(template.render(template_values))


class LanguageContributionHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('add_language.html')
        self.response.write(template.render(template_values))


class LanguageClassificationHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('add_language_classification.html')
        self.response.write(template.render(template_values))

    def post(self):
        all_request = self.request.body
        dic = json.loads(all_request)
        language = dic['language']
        all_data = dic['all_data']
        ce = ContributionEngine(language)
        res = ce.add_classification_for_language(all_data)
        response = dict()
        response['response'] = res
        json_response = json.dumps(response)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)


class LanguageUrlsHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('add_language_urls.html')
        self.response.write(template.render(template_values))

    def post(self):
        all_request = self.request.body
        dic = json.loads(all_request)
        language = dic['language']
        all_data = dic['all_data']
        ce = ContributionEngine(language)
        res = ce.add_classification_for_language(all_data)
        response = dict()
        response['response'] = res
        json_response = json.dumps(response)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)


class GetTranslation(webapp2.RequestHandler):
    def get(self):
        json_response = json.dumps(languages)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)

    def post(self):
        all_request = self.request.body
        dic = json.loads(all_request)
        lang = dic['language']
        lang = "Ruby" if lang == "Ruby-1.9" else lang
        te = TranslationEngine(lang)
        translated_text, final_code_text = te.get_translation((dic["text"]).encode('utf8'))
        response_list = []
        logging.info("in server interface " + final_code_text)
        response_list.append(final_code_text)
        response_list.append(translated_text)
        json_response = json.dumps(response_list)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)


class CheckKeyword(webapp2.RequestHandler):
    def post(self):
        dic = json.loads(self.request.body)
        keyword = dic['keyword']
        language = dic['language']
        ce = ContributionEngine(language, keyword)
        res = ce.contribute()
        logging.info("result " + res)
        response = dict()
        response['response'] = res
        json_response = json.dumps(response)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)


class Contribute(webapp2.RequestHandler):
    def post(self):
        dic = json.loads(self.request.body)
        save = dic['save']
        keyword = dic['keyword']
        language = dic['language']
        url = dic['url']
        word_type = dic['word_type']
        translation_type = dic['option']
        try:
            name = dic["name"]
        except KeyError:
            name = None
        ce = ContributionEngine(language, keyword)
        res, rc = ce.get_translation(word_type, url, translation_type, name)
        if eval(save):
            res = ce.save_in_db(word_type, url, res)
        logging.info("result " + str(res))
        response = dict()
        response['response'] = res
        response['rc'] = rc
        json_response = json.dumps(response)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)


class Approve(webapp2.RequestHandler):
    def post(self):
        dic = json.loads(self.request.body)
        keyword = dic['keyword']
        language = dic['language']
        ce = ContributionEngine(language, keyword)
        res = ce.user_approve()
        response = dict()
        response['response'] = res
        json_response = json.dumps(response)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)


class AddLanguage(webapp2.RequestHandler):
    def post(self):
        dic = json.loads(self.request.body)
        language = dic['language']
        all_data = dic['all_data']
        ce = ContributionEngine(language)
        res = ce.add_new_language(all_data)
        response = dict()
        response['response'] = res
        json_response = json.dumps(response)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)


app = webapp2.WSGIApplication([
    ('/gettranslation', GetTranslation),
    ('/contribution-page', ContributionHandler),
    ('/contribute-language', LanguageContributionHandler),
    ('/add_language_classification', LanguageClassificationHandler),
    ('/add_language_urls', LanguageUrlsHandler),
    ('/check-keyword', CheckKeyword),
    ('/contribute', Contribute),
    ('/approve', Approve),
    ('/add-language', AddLanguage),
    ('/', MainHandler)
], debug=True)
