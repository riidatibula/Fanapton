#WEB
import sys
import os

import webapp2
import jinja2
from models import Shop

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader('templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)


class MainPage(webapp2.RequestHandler):
  def get(self):
    shops = Shop.query()

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
    	'url_linktext': url_linktext,
      'shops': shops
    }

    template = JINJA_ENVIRONMENT.get_template('home.html')
    self.response.write(template.render(context))


class AddShop(webapp2.RequestHandler):
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

    template = JINJA_ENVIRONMENT.get_template('addShop.html')
    self.response.write(template.render(context))

  def post(self):
    owner = self.request.get('owner')
    name = self.request.get('name')
    contact = self.request.get('contact')
    address = self.request.get('address')
    address_list = [address]
    contact_list = [contact]

    shop = Shop(owner=owner, name=name, contacts=contact_list, address=address_list)
    shop.put()

    self.redirect('/')


app = webapp2.WSGIApplication([
	('/', MainPage),
  ('/addShop', AddShop),
], debug=True)