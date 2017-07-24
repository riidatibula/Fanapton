#WEB
import sys

import 	webapp2
import 	json

from 	google.appengine.ext 		import 	blobstore
from 	google.appengine.ext.webapp import 	blobstore_handlers
from 	google.appengine.ext 		import 	ndb

import 	jinja2
import 	os

import 	google.appengine.api.images
import firebase_admin


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


#INITIALIZE FIREBASE
# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

class Images(ndb.Model):
    image_key = ndb.BlobKeyProperty()


class MainPage(webapp2.RequestHandler):

	def get(self):
		upload_url = blobstore.create_upload_url('/upload')
		template = JINJA_ENVIRONMENT.get_template('test.html')
		self.response.write(template.render().format(upload_url))


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):

	def post(self):
		upload = self.get_uploads('file')[0]
		instance = Images(image_key=upload.key())
		instance.put()
		# self.redirect('/view_photo/%s' % upload.key())
		self.redirect('/respond')
		

class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):

    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)


class jsonReturn(webapp2.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'application/json'   
		reply = {
		  'tags': ['jacket', 'hoodie', 'black'],
		  'payload': 'some var',
		} 
		self.response.out.write(json.dumps(reply))



#FIREBASE
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('./keys/fanapton-firebase-adminsdk-73ws9-db42f04ba6.json')

# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fanapton.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
main_ref = db.reference('restricted_access/secret_document')
main_db = 'path/'


def push_data(document, data):
	db_ref = main_ref.child(document)
	db_ref.push(data)

def update_data(document, query, data):
	db_ref = main_ref.child(document)
	db_ref.child(query).update(data)

def get_data(document, query):
	ref_str = main_db + document
	ref = db.reference(ref_str)
	return ref.get()


app = webapp2.WSGIApplication([

	('/', MainPage),
	('/upload', PhotoUploadHandler),
	('/view_photo/([^/]+)?', ViewPhotoHandler),
	('/respond', jsonReturn)

], debug=True)