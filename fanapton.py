#WEB
import sys
import os

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader('templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

class Main(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('home.html')
		self.response.write(template.render())

app = webapp2.WSGIApplication([
	('/', Main),
], debug=True)
