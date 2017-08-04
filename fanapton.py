#WEB
import sys
import os

import webapp2
import jinja2

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader('templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)


class MainPage(webapp2.RequestHandler):
  def get(self):

    user = users.get_current_user()

    if user:
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'login'

    context = {
    	'user': user,
    	'url': url,
    	'url_linktext': url_linktext
    }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(context))


app = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)