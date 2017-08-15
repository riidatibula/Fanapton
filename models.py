from google.appengine.ext import ndb

class Apparel(ndb.Model):
	name = ndb.StringProperty()
	parsed_name = ndb.StringProperty()
	image = ndb.StringProperty(indexed=False)
	tags = ndb.StringProperty(indexed=False, repeated=True)
	description = ndb.StringProperty(indexed=False)
	price = ndb.IntegerProperty(indexed=False)

class Shop(ndb.Model):
	name = ndb.StringProperty(required=True)
	about = ndb.StringProperty(indexed=False, required=True)
	overview = ndb.StringProperty(indexed=False, required=True)
	address = ndb.StringProperty(indexed=False, repeated=True)
	emails = ndb.StringProperty(indexed=False, repeated=True)
	websites = ndb.StringProperty(indexed=False, repeated=True)
	awards = ndb.StringProperty(indexed=False, repeated=True) 
	date_joined = ndb.DateTimeProperty(auto_now_add=True)
	cover_image = ndb.StringProperty(indexed=False)
	profile_image = ndb.StringProperty(indexed=False)
	apparels = ndb.LocalStructuredProperty(Apparel, repeated=True)

class Cart(ndb.Model):
	user_id = ndb.IntegerProperty(indexed=True, required=True),
	apparels = ndb.LocalStructuredProperty(Apparel, repeated=True)

