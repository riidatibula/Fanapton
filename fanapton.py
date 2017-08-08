#WEB
import sys
import os

import webapp2
import jinja2
import cloudstorage as gcs
import six

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from models import Shop

#Configure Jinja
JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader('templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

#Get the default bucket from google cloud storage
default_bucket = 'fanapton.appspot.com'

def upload_file(file):
  uploaded_file_content = file.file.read()
  uploaded_file_filename = file.filename
  uploaded_file_type = file.type

  write_retry_params = gcs.RetryParams(backoff_factor=1.1)
  gcs_file = gcs.open(
    "/" + default_bucket + "/" + uploaded_file_filename,
    "w",
    content_type=uploaded_file_type,
    retry_params=write_retry_params
  )
  gcs_file.write(uploaded_file_content)
  gcs_file.close()
  return get_file_url(uploaded_file_filename)


def get_file_url(uploaded_file_filename):
  file_url = 'https://%(bucket)s.storage.googleapis.com/%(file)s' % {'bucket':default_bucket, 'file':uploaded_file_filename}
  return file_url


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
      url = users.create_logout_url('/')
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
    image = self.request.POST.get('image')
    address_list = [address]
    contact_list = [contact]
    image_url = upload_file(image)

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
      url_linktext = 'logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'login'

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


app = webapp2.WSGIApplication([
	('/', MainPage),
  ('/addShop', AddShop),
  ('/shopDetails/(?P<url_string>[\w\-]+)', ShopDetails),
  ('/deleteShop/(?P<url_string>[\w\-]+)', DeleteShop)
], debug=True)