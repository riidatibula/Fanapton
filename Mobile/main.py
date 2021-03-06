#MOBILE
import sys
import os

import webapp2
import json
import jinja2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from google.appengine.api import users

import google.appengine.api.images
import firebase_admin


JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader('templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

# GCLOUD STORAGE
# from google.cloud import storage
import cloudstorage as gcs
# Reference an existing bucket.
BUCKET_NAME = 'fanapton.appspot.com'

class Home(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('home.html')
		self.response.write(template.render())


class AnotherPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('anotherPage.html')
		self.response.write(template.render())


class Images(ndb.Model):
  image_key = ndb.BlobKeyProperty()


class MainPage(webapp2.RequestHandler):
	def get(self):
		# upload_url = blobstore.create_upload_url('/upload')
		template = JINJA_ENVIRONMENT.get_template('test.html')
		self.response.write(template.render())


# class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):

# 	def post(self):
# 		upload = self.get_uploads('file')[0]
# 		instance = Images(image_key=upload.key())
# 		instance.put()
# 		# self.redirect('/view_photo/%s' % upload.key())
# 		self.redirect('/respond')

class PhotoUploadHandler(webapp2.RequestHandler):
	def post(self):
		print "TO UPLOAD"
		uploaded_file = self.request.POST.get("file")
		uploaded_file_content = uploaded_file.file.read()
		uploaded_file_filename = uploaded_file.filename
		uploaded_file_type = uploaded_file.type

		write_retry_params = gcs.RetryParams(backoff_factor=1.1)
		gcs_file = gcs.open(
        "/" + BUCKET_NAME + "/" + uploaded_file_filename,
        "w",
        content_type=uploaded_file_type,
        retry_params=write_retry_params
	    )
		gcs_file.write(uploaded_file_content)
		gcs_file.close()
		param = '' + BUCKET_NAME + '/' + uploaded_file_filename
		self.redirect('/view_photo/%s' % param)
		# self.redirect('/respond')


# class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):

#     def get(self, photo_key):
# 			print "VIEW NA BES"
# 			if not blobstore.get(photo_key):
# 				self.error(404)
# 			else:
# 				self.send_blob(photo_key)

class ViewPhotoHandler(webapp2.RequestHandler):
	def get(self, filename):
		# with gcs.open(filename) as cloudstorage_file:
		# 	self.response.write(cloudstorage_file.readline())
		# 	cloudstorage_file.seek(-1024, os.SEEK_END)
		# 	self.response.write(cloudstorage_file.read())
		cloudstorage_file = gcs.open(filename)
		self.response.write(cloudstorage_file)

class jsonReturn(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'   
		reply = {
		  'tags': ['jacket', 'hoodie', 'black'],
		  'payload': 'some var',
		
		self.response.out.write(json.dumps(reply))

app = webapp2.WSGIApplication([
	(r'/Mobile/home', Home),
	(r'/Mobile/testupload', MainPage),
	(r'/Mobile/upload', PhotoUploadHandler),
	(r'/Mobile/view_photo/([^/]+)?', ViewPhotoHandler),
	(r'/Mobile/respond', jsonReturn),
], debug=True)