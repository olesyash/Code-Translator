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
import logging
import jinja2
from translation_engine.translation_engine import *
from engine.result_parser import *
from translation_engine.languages_specific_features import *



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

    def post(self):
        pass


class GetTranslation(webapp2.RequestHandler):
    def get(self):
        json_response = json.dumps(languages)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)

    def post(self):
        code_text = self.request.body
        dic = json.loads(code_text)
        te = TranslationEngine(dic['language'])
        response_list = []
        translated_text, final_code_text = te.get_translation((dic["text"]).encode('utf8'))
        logging.info("in server interface " + final_code_text)
        response_list.append(final_code_text)
        response_list.append(translated_text)
        json_response = json.dumps(response_list)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_response)



app = webapp2.WSGIApplication([
    ('/gettranslation', GetTranslation),
    ('/', MainHandler)
], debug=True)
