import mongoengine as me
import jwt
from dotenv import load_dotenv
import os
from bson import ObjectId
import bson

from my_loc8r_app_glennc15.app_api.models.location_models import Locations

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class APIControllersBase(object):
	'''
	
	Base class for all controllers.


	This class also contains some helper methods that are usefull to all controllers


	'''


	def __init__(self):

		self.status_code = None 
		self.data = None


	@property
	def status_code(self):
		return self._status_code 

	@status_code.setter
	def status_code(self, value):
		self._status_code = value


	@property
	def html(self):
		return self._html 

	@html.setter
	def html(self, value):
		self._html = value

	# data is an alias for html. data makes more since to use in an api.
	@property
	def data(self):
		return self.html 

	@data.setter
	def data(self, value):
		self.html = value


	# *******************************************************************************
	# START: helper methods:		

	def common_validation_errors(self, exception):
		'''


		'''

		if isinstance(exception, me.errors.ValidationError):
			self.data = {'error': "{}".format(exception)}
			self.status_code = 400

		elif isinstance(exception, KeyError):
			self.data = {'error': "{} filed is reqired".format(exception)}
			self.status_code = 400

		elif isinstance(exception, Locations.DoesNotExist):
			self.data = {'error': "No record found. {}".format(exception)}
			self.status_code = 404

		elif isinstance(exception, me.errors.OperationError):
			self.data = {'error': "{}".format(exception)}
			self.status_code = 400

		elif isinstance(exception, ValueError):
			self.data = {'error': "{}".format(exception)}
			self.status_code = 400

		elif isinstance(exception, bson.errors.InvalidId):
			self.data = {'error': "{}".format(exception)}
			self.status_code = 400


		else:
			print("exception = {}".format(exception))
			raise exception 


	def format_location(self, document):
		'''


		'''
		# remove the object ids:
		location_data =  self.convert_object_ids(document=document)

		# seperate 'coords' into longatude and lattitude and then remove 'coords'
		location_data['lng'] = location_data['coords']['coordinates'][0]
		location_data['lat'] = location_data['coords']['coordinates'][1]

		# remove coords from dictionary:
		location_data = dict([(k, v) for k, v in location_data.items() if k not in ['coords']])


		return location_data



	def convert_object_ids(self, document):
		'''
		
		Mongo ObjectId cannot be converted to JSON.

		Each Mongoengine Document class has a .to_json() method but it converts
		ObjectIds to {'$oid': '6408a9dcdec8287c6dfd03d6'}
		
		So converts all ObjectId objects to strings

		'''

		if isinstance(document, dict):
			record = document

		else:
			record = document.to_mongo().to_dict()


		# Convert Location ObjectIds:
		for key1, value1 in record.items():
			if isinstance(value1, ObjectId):
				record[key1] = str(value1)




		# convert the ObjectId for each opeing time sub document
		if record.get('openingTimes'):
			for opening_time in record['openingTimes']:
				for o_key, o_value in opening_time.items():
					if isinstance(o_value, ObjectId):
						opening_time[o_key] = str(o_value) 


		# convert the ObjectId for each review sub document
		# pdb.set_trace()

		if record.get('reviews'):
			for review in record['reviews']:
				for r_key, r_value in review.items():
					if isinstance(r_value, ObjectId):
						review[r_key] = str(r_value)



		return record 




	def is_object_id_ok(self, request, object_id):
		'''

		Validate object_id is ObjectId object. Any invalid object_id is a 401 error.


		'''

		if not bson.objectid.ObjectId.is_valid(object_id):

			scheme, netloc, path, query, fragment = urlsplit(request.base_url)

			error_msg = "{} {}{} is not valid\n".format(request.method, path, query)
			error_msg += "{} is not a valid id".format(object_id)

			self.data = {'message': error_msg}
			self.status_code = 404

			return False 

		return True





	def get_location_rating(self, location_obj):
		'''


		'''

		rating = 0

		if len(location_obj.reviews) > 0:
			for review in location_obj.reviews:
				rating += review.rating 

			rating /= len(location_obj.reviews)

			rating = int(rating)

		return rating




	def decode_token(self, token):
		'''

		'''
		load_dotenv()

		return jwt.decode(token, self._encode_key, algorithms=["HS256"])





	# End: helper methods:
	# *******************************************************************************











	