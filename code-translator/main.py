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
import webapp2
from DAL import *
import jinja2
import logging
import os
from engine.languages_API import *
from translation_engine.translation_engine import *
from engine.result_parser import *


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader("web"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def show_data(self, keyword):
        a = LanguagesAPI()
        language = "python"
        link = "https://docs.python.org/2/reference/compound_stmts.html#the-for-statement"
        result, code = a.http_request_using_urlfetch(link, {})
        b = ResultParser()
        res = b.find_by_id(result, 'the-for-statement')
        logging.info("result is " + res)
        try:
            DAL.save_data_in_db("python", keyword, "statement", link, res)
        except DataExistException:
            pass

        cntb = "for"  # code needed to be translated
        link = "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/for.html"
        result, code = a.http_request_using_urlfetch(link, {})
        clean_text = b.find_by_id(result, 'PageContent')
        logging.info("result is " + clean_text)

        try:
            DAL.save_data_in_db("java", cntb, "statement", link, clean_text)
        except DataExistException:
            pass

    def get(self):
        logging.info("Main handler: loading landing page")
        try:
            self.show_data("for")
        except DataExistException:
            logging.info("data already exist")

        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        pass


class GetTranslation(webapp2.RequestHandler):
    def get(self):
        pass

    def post(self):
        code_text = self.request.body
        translation_text = TranslationEngine.get_translation(code_text, "python") # TODO: Need to add language treatment
        json_response = json.dumps(translation_text)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)



app = webapp2.WSGIApplication([
    ('/gettranslation', GetTranslation),
    ('/', MainHandler)
], debug=True)
