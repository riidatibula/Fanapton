#WEB
import sys
import os

import webapp2
import jinja2
import storage
import json

from google.appengine.api import users
from google.appengine.ext import ndb
from models import Shop
from models import Apparel
from models import Cart

#Configure Jinja
JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader('templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)


class MainPage(webapp2.RequestHandler):
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
      'url_linktext': url_linktext,
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
    name = self.request.POST.get('name')
    about = self.request.POST.get('about')
    overview = self.request.POST.get('overview')
    address = self.request.POST.get('address')
    email = self.request.POST.get('email')
    website = self.request.POST.get('website')
    award = self.request.POST.get('award')
    cover_image = self.request.POST.get('cover_image')
    profile_image = self.request.POST.get('profile_image')

    address_list = [address]
    email_list = [email]
    website_list = [website]
    award_list = [award]
    cover_image_url = storage.upload_file(cover_image)
    profile_image_url = storage.upload_file(profile_image)

    shop = Shop(name=name, about=about, overview=overview, address=address_list, emails=email_list, 
      websites=website_list, awards=award_list, cover_image=cover_image_url, profile_image=profile_image_url)
    shop.put()

    self.redirect('/allShops')


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


class Products(webapp2.RequestHandler):
  def get(self, url_string):
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

    template = JINJA_ENVIRONMENT.get_template('products.html')
    self.response.write(template.render(context))


class DeleteShop(webapp2.RequestHandler):
  def post(self, url_string):
    shop_key = ndb.Key(urlsafe=url_string)
    shop_key.delete()

    self.redirect('/allShops')


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
      url_linktext = 'Log in'

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

    data = name.split(" ")

    if len(data) > 1:
      parsed_name = "_".join(data)
    elif len(data) == 1:
      parsed_name = data[0]

    apparel = Apparel(name=name, parsed_name=parsed_name, image=image_url, price=price, description=desc)
    apparel.put()

    shop.apparels.append(apparel)
    shop.put()

    self.redirect('/allShops')


class ApparelDetails(webapp2.RequestHandler):
  def get(self, url_safe, apparel_name):
    shop_key = ndb.Key(urlsafe=url_safe)
    shop = shop_key.get()

    apparel = Apparel.query(Apparel.parsed_name == apparel_name).get()

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
      'shop': shop,
      'apparel': apparel
    }

    template = JINJA_ENVIRONMENT.get_template('apparelDetails.html')
    self.response.write(template.render(context))


class DeleteApparel(webapp2.RequestHandler):
  def post(self, url_safe, apparel_url_safe):
    shop_key = ndb.Key(urlsafe=url_safe)
    shop = shop_key.get()

    apparel_key = ndb.Key(urlsafe=apparel_url_safe)
    apparel = apparel_key.get()

    shop.apparels = [i for i in shop.apparels if i.parsed_name != apparel.parsed_name]
    shop.put()
    
    apparel_key.delete()
    
    self.redirect('/allShops')


class MyCart(webapp2.RequestHandler):
  def get(self, user_id):

    user = users.get_current_user()

    if user:
      url = users.create_logout_url('/')
      url_linktext = 'Log out'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Log In'

    context = {
      'user': user,
      'url': url,
      'url_linktext': url_linktext,
    }

    template = JINJA_ENVIRONMENT.get_template('myCart.html')
    self.response.write(template.render(context))


class AllShops(webapp2.RequestHandler):
  def get(self):
    shops = Shop.query()

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
      'shops': shops
    }

    template = JINJA_ENVIRONMENT.get_template('shops.html')
    self.response.write(template.render(context))


class SearchShop(webapp2.RequestHandler):
  def post(self):
    shops = Shop.query()
    location = self.request.POST.get('location')
    
    if location:
      result = []
      location = location.upper()
      for shop in shops:
        for address in shop.address:
          if location in address.upper():
            result.append(shop)
            break
      shops = result

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
      'location': location,
      'shops': shops
    }

    template = JINJA_ENVIRONMENT.get_template('shops.html')
    self.response.write(template.render(context))


class GoogleSearchConsole(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('google7f04c06b777bcd27.html')
    self.response.write(template.render())


class GoogleSearchConsole2(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('google66a09b8269578bf4.html')
    self.response.write(template.render())


class GHomeSearch(webapp2.RequestHandler):
  def post(self, location):
    shops = Shop.query()

    result = []
    location = location.upper()

    for shop in shops:
      for address in shop.address:
        if location in address.upper():
          result.append(shop)
          break
    shops = result

    self.response.headers['Content-Type'] = 'application/json'

    context={}

    if len(shops) > 0:
      name = shops[0].name
      about = shops[0].about
      overview = shops[0].overview
      address = shops[0].address[0]
      emails = shops[0].emails[0]

      context = {
        'name': name,
        'about': about,
        'overview': overview,
        'address': address,
        'emails': emails
      }

    self.response.out.write(json.dumps(context))

  def get(self, location):
    shops = Shop.query()

    result = []
    location = location.upper()

    for shop in shops:
      for address in shop.address:
        if location in address.upper():
          result.append(shop)
          break
    shops = result

    self.response.headers['Content-Type'] = 'application/json'

    context={}

    if len(shops) > 0:
      name = shops[0].name
      about = shops[0].about
      overview = shops[0].overview
      address = shops[0].address[0]
      emails = shops[0].emails[0]

      context = {
        'name': name,
        'about': about,
        'overview': overview,
        'address': address,
        'emails': emails
      }

    self.response.out.write(json.dumps(context))


app = webapp2.WSGIApplication([
	('/', MainPage),
  ('/google7f04c06b777bcd27.html', GoogleSearchConsole),
  ('/google66a09b8269578bf4.html', GoogleSearchConsole2),
  ('/allShops', AllShops),
  ('/searchShops', SearchShop),
  ('/gHome/search/(?P<lcocation>[\w\-]+)', GHomeSearch),
  ('/addShop', AddShop),
  ('/shopDetails/(?P<url_string>[\w\-]+)/', ShopDetails),
  ('/shopDetails/(?P<url_string>[\w\-]+)/products/', Products),
  ('/deleteShop/(?P<url_string>[\w\-]+)', DeleteShop),
  ('/addApparel/(?P<url_string>[\w\-]+)', AddApparel),
  ('/shopDetails/(?P<url_safe>[\w\-]+)/(?P<apparel_name>[\w\-]+)/', ApparelDetails),
  ('/shopDetails/(?P<url_safe>[\w\-]+)/(?P<apparel_name>[\w\-]+)/deleteApparel/', DeleteApparel),
  ('/myCart/(?P<user_id>\d+)/', MyCart),
], debug=True)