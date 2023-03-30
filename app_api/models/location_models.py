import mongoengine as me
import datetime
from bson import ObjectId

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class Review(me.EmbeddedDocument):
	_id = me.ObjectIdField(required=True, default=ObjectId)
	author = me.StringField(required=True, min_length=2)
	author_id = me.ObjectIdField(required=True)
	rating = me.IntField(required=True, min_value=1, max_value=5)
	review_text = me.StringField(required=True, min_length=2)
	created_on = me.DateTimeField(default=datetime.datetime.utcnow)


class OpeningTime(me.EmbeddedDocument):
	_id = me.ObjectIdField(required=True, default=ObjectId)
	days = me.StringField(required=True)
	opening = me.StringField()
	closing = me.StringField()
	closed = me.BooleanField(required=True)


	@ staticmethod
	def validate_doc(doc):
		'''
		


		'''

		# check .opening and .closing are valid strings when .closed = False
		if doc.closed == False:

			if (doc.opening is None):
				raise me.errors.ValidationError("field ['opening'] is required when field ['closed'] = True")

			elif (isinstance(doc.opening, str) and (len(doc.opening)==0)):
				raise me.errors.ValidationError("field ['opening'] is cannot be empty when field ['closed'] = True")

			elif (doc.closing is None):
				raise me.errors.ValidationError("field ['closing'] is required when field ['closed'] = True")

			elif (isinstance(doc.closing, str) and (len(doc.closing)==0)):
				raise me.errors.ValidationError("field ['closing'] is cannot be empty when field ['closed'] = True")



	def clean(self):
		'''


		'''

		self.validate_doc(doc=self)




class Locations(me.Document):
	name = me.StringField(required=True, min_length=1)
	address = me.StringField(min_length=1)
	rating = me.IntField(default=0, min_value=0, max_value=5)
	facilities = me.StringField()
	coords = me.PointField(auto_index=True)
	openingTimes = me.ListField(me.EmbeddedDocumentField(OpeningTime))
	reviews = me.ListField(me.EmbeddedDocumentField(Review))
	views = me.IntField(default=0)
	
	# opening_times = me.EmbeddedDocumentListField(me.EmbeddedDocument(OpeningTimeSchema))
	# reviews = me.EmbeddedDocumentListField(me.EmbeddedDocument(ReviewSchema))






	# @staticmethod
	def validate_coods(self, coords):

		if isinstance(coords, list):
			longitude, latitude = coords

		elif isinstance(coords, dict):
			longitude, latitude = coords['coordinates']


		# print("type(longitude) = {}".format(type(longitude)))
		# print("type(latitude) = {}".format(type(latitude)))
		# print("coords = {}".format(coords))

		# pdb.set_trace()
		
		if not (-180.0<=longitude<=180.0):
			raise me.errors.ValidationError("longitude = {} is out of range, -180.0 <= longitude <= 180".format(longitude))

		if not (-90.0<=latitude<=90.0):
			raise me.errors.ValidationError("latitude = {} is out of range, -90.0 <= latitude <= 90".format(latitude))




	def clean(self):
		'''


		'''

		self.validate_coods(self.coords)




