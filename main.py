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

import datetime
import os
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template



class Conversation(db.Model):
    
    fromText = db.StringProperty(required=True)
    date = db.DateProperty()
    toText = db.StringProperty(required=True)

class MainHandler(webapp.RequestHandler):
    def get(self):
       
       conversations_query = Conversation.all().order('-date')
       conversations = conversations_query.fetch(10)
       
       template_values = {
              'conversations' : conversations 
         }
       
       r = self.request
       conversation = Conversation(fromText = r.get('from'), 
                                    toText = r.get('to'),
                                    date = datetime.datetime.now().date())
       
       conversation.put()
       
       path = os.path.join(os.path.dirname(__file__), 'index.html')
       self.response.out.write(template.render(path, template_values))
       
#       self.response.out.write('<html><body>')
#       self.response.out.write(conversation.fromText + '</br>' + conversation.toText + '</br>' )
#       self.response.out.write( conversation.date)
#       self.response.out.write('</body></html>')
       


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
