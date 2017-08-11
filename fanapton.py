#WEB
import sys
import os

import webapp2
import jinja2
import storage

from google.appengine.api import users
from google.appengine.ext import ndb
from models import Shop
from models import Apparel

#Configure Jinja
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
      url_linktext = 'Log out'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Log in'

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
      url = users.create_logout_url('/')
      url_linktext = 'Log out'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Log in'

    context = {
      'user': user,
      'url': url,
      'url_linktext': url_linktext
    }

    template = JINJA_ENVIRONMENT.get_template('addShop.html')
    self.response.write(template.render(context))

  def post(self):
    owner = self.request.POST.get('owner')
    name = self.request.POST.get('name')
    contact = self.request.POST.get('contact')
    address = self.request.POST.get('address')
    image = self.request.POST.get('image')
    address_list = [address]
    contact_list = [contact]
    image_url = storage.upload_file(image)

    shop = Shop(owner=owner, name=name, contacts=contact_list, address=address_list, image=image_url)
    shop.put()

    self.redirect('/')


class ShopDetails(webapp2.RequestHandler):
  def handle_requests(self, url_string):
    shop_key = ndb.Key(urlsafe=url_string)
    shop = shop_key.get()

    user = users.get_current_user()

    if user:
      url = users.create_logout_url('/')
      url_linktext = 'Log out'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Log in'

    context = {
      'user': user,
      'url': url,
      'url_linktext': url_linktext,
      'shop': shop
    }

    template = JINJA_ENVIRONMENT.get_template('shopDetails.html')
    self.response.write(template.render(context))

  def post(self, url_string):
    self.handle_requests(url_string)

  def get(self, url_string):
    self.handle_requests(url_string)


class DeleteShop(webapp2.RequestHandler):
  def post(self, url_string):
    shop_key = ndb.Key(urlsafe=url_string)
    shop_key.delete()

    self.redirect('/')


class AddApparel(webapp2.RequestHandler):
  def get(self, url_string):
    shop_key = ndb.Key(urlsafe=url_string)
    shop = shop_key.get()

    user = users.get_current_user()

    if user:
      url = users.create_logout_url('/')
      url_linktext = 'Log out'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'log in'

    context = {
      'user': user,
      'url': url,
      'url_linktext': url_linktext,
      'shop': shop
    }

    template = JINJA_ENVIRONMENT.get_template('addApparel.html')
    self.response.write(template.render(context))

  def post(self, url_string):
    shop_key = ndb.Key(urlsafe=url_string)
    shop = shop_key.get()

    name = self.request.POST.get('name')
    price = int(self.request.POST.get('price'))
    image = self.request.POST.get('image')
    desc = self.request.POST.get('desc')
    image_url = storage.upload_file(image)
    tags = []

    apparel = Apparel(name=name, image=image_url, price=price, description=desc)
    apparel.put()

    shop.apparels.append(apparel)
    shop.put()

    self.redirect('/')


app = webapp2.WSGIApplication([
	('/', MainPage),
  ('/addShop', AddShop),
  ('/shopDetails/(?P<url_string>[\w\-]+)', ShopDetails),
  ('/deleteShop/(?P<url_string>[\w\-]+)', DeleteShop),
  ('/addApparel/(?P<url_string>[\w\-]+)', AddApparel)
], debug=True)