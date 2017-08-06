from google.appengine.ext import ndb

class Apparel(ndb.Model):
	name = ndb.StringProperty(indexed=False)
	image = ndb.StringProperty(indexed=False)
	tags = ndb.StringProperty(indexed=False, repeated=True)
	price = ndb.IntegerProperty(indexed=False)

class Shop(ndb.Model):
	owner = ndb.StringProperty(indexed=False, required=True)
	name = ndb.StringProperty(indexed=False, required=True)
	address = ndb.StringProperty(indexed=False, repeated=True)
	contacts = ndb.StringProperty(indexed=False, repeated=True)
	date_joined = ndb.DateTimeProperty(auto_now_add=True)
	image = ndb.StringProperty(indexed=False)
	apparels = ndb.LocalStructuredProperty(Apparel, repeated=True)