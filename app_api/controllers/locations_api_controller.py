from urllib.parse import urlsplit
import bson
from bson import ObjectId
import re 
import json
import mongoengine as me


from my_loc8r.app_api.controllers.api_controllers_base import APIControllersBase
from my_loc8r.app_api.models.location_models import Locations, OpeningTime

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class LocationsAPIController(APIControllersBase):
	'''
	
	Controller class for all API routes.

	'''

	def __init__(self):
		'''

		'''

		super().__init__()

		

		self._required_location_keys = ['name', 'lng', 'lat']
		self._required_opening_keys = ['closed', 'days']
		





	# *******************************************************************************
	# START: Public methods:



	# POST:/api/locations
	def create_location(self, location_data):
		'''

		'''

		# Build a location model instance with only the location data
		# (no opening times). Then add the longitude and lattitude data

		location = Locations(**dict([(k, v) for k, v in location_data.items() if k in ['name', 'address', 'rating', 'facilities']]))

		# if longiture or lattiude is missing it will raise a key error. Any
		# key error will generates a 400 response
		try:
			location.coords = [location_data['lng'], location_data['lat']]

		except Exception as e:
			self.common_validation_errors(e)
			return None 


		# build opening time sub documents:
		if location_data.get('openingTimes'):

			# I know I should NOT write this in one line but I can't help myself! :)
			location.openingTimes = [OpeningTime(**dict([(k, v) for k, v in opening_time.items() if k in ['days', 'opening', 'closing', 'closed']])) for opening_time in location_data['openingTimes']]
			
			# opening_time_records = list()
			
			# for opening_time in location_data['openingTimes']:
			# 	this_opening_time = OpeningTime(**dict([(k, v) for k, v in opening_time.items() if k in ['days', 'opening', 'closing', 'closed']]))

			# 	try:
			# 		# this_opening_time.validate()
			# 		pass 

			# 	except Exception as e:
			# 		self.common_validation_errors(e)
			# 		return None 

			# 	opening_time_records.append(this_opening_time)

			# location.openingTimes = opening_time_records



		try:
			location.save()

		except Exception as e:
			self.common_validation_errors(e)
			return None 


		self.data = self.format_location(document=location)
		self.status_code = 201


	# GET:/api/locations
	def read_locations_by_distance(self, parameters):
		'''

		'''
		
		longitude, latitude, max_dist = self.parse_location_parameters(parameters=parameters)

		# print('longitude = {}'.format(longitude))
		# print('latitude = {}'.format(latitude))
		print('max_dist = {}'.format(max_dist))


		if (longitude is not None) and (latitude is not None):
			
			start_point = {
				'type': 'Point',
				'coordinates': [longitude, latitude]
				# 'coordinates': [latitude, longitude]

			}

			# max_dist is in km. Must be converted to m:
			max_dist_m = max_dist * 1000

			# distances are returned in m. So convert them to km
			# with 'distanceMultiplier' = 1/0000
			pipeline = [
				{
					'$geoNear': {
						'near': start_point,
						'spherical': True,
						'distanceField': 'dist_calc',
						'maxDistance': max_dist_m,
						'distanceMultiplier': 1/1000,
						'key': 'coords'
					}
				}
			]


			locations = Locations.objects().aggregate(pipeline)

			self.data = [self.format_location(document=x) for x in locations]
			self.status_code = 200



	# GET:/api/locations/<locationid>
	def read_location_by_id(self, location_id):
		'''

		'''


		try:
			location = Locations.objects(id=location_id).get()
			
		except Exception as e:
			self.common_validation_errors(e)
			return None 


		self.data = self.format_location(document=location)
		self.status_code = 200
				



	# PUT:/api/locations/<locationid>
	def update_location(self, location_id, location_data):
		'''




		'''
		# Find the location by id:
		try:
			location = Locations.objects(id=location_id).get()

		except Exception as e:

			error_msg = "No location record with id = {} found.".format(location_id)
			self.data = {'message': error_msg}
			self.status_code = 404

			return None

		# update the Location record:
		location.name = new_data['name']
		location.address = new_data['address']
		location.facilities = new_data['facilities']
		location.coords = [new_data['lng'], new_data['lat']]

		opening_time_records = self.build_opening_times(opening_times_list=new_data['openingTimes'])
		location.openingTimes = opening_time_records

		try:
			location.save()
			location_data = self.format_location(document=location)

			self.data = location_data
			self.status_code = 200

		except Exception as e:
			# not sure how to test this
			print("500 Error!")
			print(e)

			self.data = {'message': 'database error!'}
			self.status_code = 500

		return None 


	# DELETE:/api/locations/<locationid>
	def delete_location(self, location_id):
		'''

		'''

		try:
			location = Locations.objects(id=location_id).get().delete()
			self.data = {'message': "location with id = {} was successfully removed".format(location_id)}
			self.status_code = 204

		except Exception as e:
			# not sure how to test this
			print("500 Error!")
			print(e)

			self.data = {'message': 'database error!'}
			self.status_code = 500

		return None 



	# End: Public methods:
	# *******************************************************************************


	def parse_location_parameters(self, parameters):
		'''


		'''



		for coords_key in ['lng', 'lat']:
			if coords_key not in parameters:
				error_msg = "{} is a required parameter and is missing in the query".format(coords_key)

				self.data = {"message": error_msg}
				self.status_code = 404

				return (None, None, None)

		# print('parameters = '.format(parameters))
		# pdb.set_trace()

		# validate the latitude parameter:
		try:
			latitude = float(parameters['lat'])

		except Exception as e:
			error_msg = "the parameter['lat'] = {} is not a float.".format(parameters['lat'])
			self.data = {"message": error_msg}
			self.status_code = 404
			
			return (None, None, None)

		if not self.is_latitude_ok(latitude=latitude):
			latitude = None 


		# validate the longitude parameter:
		try:
			longitude = float(parameters['lng'])

		except Exception as e:
			error_msg = "the parameter['lng'] = {} is not a float.".format(parameters['lng'])
			self.data = {"message": error_msg}
			self.status_code = 404
			
			return (None, None, None)

		if not self.is_longitude_ok(longitude=longitude):
			longitude = None


		if parameters.get('maxDistance'):
			max_dist = float(parameters['maxDistance'])

		else:
			max_dist = 1000000


		return (longitude, latitude, max_dist)	




	def is_location_data_ok(self, location_data):
		'''

		'''

		# check location data for the required values:
		for location_key in self._required_location_keys:
			if location_key not in location_data:
				error_msg = "Invalid data for location.\n"
				error_msg += "location['{}'] is required.".format(location_key)

				self.data = {"message": error_msg}
				self.status_code = 400

				return False

		# validate location_data['name']: 
		if (isinstance(location_data['name'], str)):
			if len(location_data['name']) == 0:
				error_msg = "Invalid data for location['name'].\n"
				error_msg += "location['name'] an empty string."

				self.data = {"message": error_msg}
				self.status_code = 400

				return False

		else:
				error_msg = "location['name'] must be a string.\n"
				error_msg += "location['name'] is type {}".format(type(location_data['name']))

				self.data = {"message": error_msg}
				self.status_code = 400

				return False


		# validate location_data['lng']: 
		if (isinstance(location_data['lng'], float)):
			if -180 <= location_data['lng'] <= 180:
				pass

			else:
				error_msg = "Invalid data for location['lng'] = {}.\n".format(location_data['lng'])
				error_msg += "location['lng'] must be between -180 and 180"

				self.data = {"message": error_msg}
				self.status_code = 400

				return False

		else:
				error_msg = "location['lng'] must be a float.\n"
				error_msg += "location['lng'] is type {}".format(type(location_data['lng']))

				self.data = {"message": error_msg}
				self.status_code = 400

				return False

		# validate location_data['lat']: 
		if (isinstance(location_data['lat'], float)):
			if -90 <= location_data['lat'] <= 90:
				pass

			else:
				error_msg = "Invalid data for location['lat'] = {}.\n".format(location_data['lat'])
				error_msg += "location['lat'] must be between -90 and 90"

				self.data = {"message": error_msg}
				self.status_code = 400

				return False

		else:
				error_msg = "location['lat'] must be a float.\n"
				error_msg += "location['lat'] is type {}".format(type(location_data['lat']))

				self.data = {"message": error_msg}
				self.status_code = 400

				return False



		return True

	# def is_latitude_ok(self, latitude):
	# 	'''


	# 	'''

	# 	# validate location_data['lat']: 
	# 	if (isinstance(latitude, float)):
	# 		if -90 <= latitude <= 90:
	# 			pass

	# 		else:
	# 			error_msg = "Invalid data for location['lat'] = {}.\n".format(latitude)
	# 			error_msg += "location['lat'] must be between -90 and 90"

	# 			self.data = {"message": error_msg}
	# 			self.status_code = 404

	# 			return False

	# 	else:
	# 			error_msg = "location['lat'] must be a float.\n"
	# 			error_msg += "location['lat'] is type {}".format(type(latitude))

	# 			self.data = {"message": error_msg}
	# 			self.status_code = 404

	# 			return False


	# 	return True


	# def is_longitude_ok(self, longitude):
	# 	'''

	# 	'''
	# 	# validate location_data['lng']: 
	# 	if (isinstance(longitude, float)):
	# 		if -180 <= longitude <= 180:
	# 			pass

	# 		else:
	# 			error_msg = "Invalid data for location['lng'] = {}.\n".format(longitude)
	# 			error_msg += "location['lng'] must be between -180 and 180"

	# 			self.data = {"message": error_msg}
	# 			self.status_code = 404

	# 			return False

	# 	else:
	# 			error_msg = "location['lng'] must be a float.\n"
	# 			error_msg += "location['lng'] is type {}".format(type(longitude))

	# 			self.data = {"message": error_msg}
	# 			self.status_code = 404

	# 			return False


	# 	return True



	def is_opening_data_ok(self, opening_data):
		'''

		'''

		if not isinstance(opening_data, list):
			opening_data = [opening_data]

		for opening_record in opening_data:
			if not self.is_opening_record_ok(opening_record=opening_record):
				return False


		return True


	def is_opening_record_ok(self, opening_record):
		'''


		'''

		# check opening record is a dict:
		if not isinstance(opening_record, dict):
			error_msg = "Invalid type for opening time record.\n"
			error_msg += "This opening time record is of type {}".format(type(opening_record))

			self.data = {"message": error_msg}
			self.status_code = 400

			return False


		# check opening data for the required values:
		for opening_key in self._required_opening_keys:
			if opening_key not in opening_record:
				error_msg = "Invalid data for opening time.\n"
				error_msg += "opening_time['{}'] is required.".format(opening_key)

				self.data = {"message": error_msg}
				self.status_code = 400

				return False

		# validate opening_record['days']: 
		if (isinstance(opening_record['days'], str)):
			if len(opening_record['days']) == 0:
				error_msg = "Invalid data for opening_record['days'].\n"
				error_msg += "opening_record['days'] an empty string."

				self.data = {"message": error_msg}
				self.status_code = 400
				location_data_ok = False

				return location_data_ok

		else:
				error_msg = "opening_record['days'] must be a string.\n"
				error_msg += "opening_record['days'] is type {}".format(type(opening_record['days']))

				self.data = {"message": error_msg}
				self.status_code = 400
				location_data_ok = False

				return location_data_ok

		# validate opening_record['closed']: 
		if not (isinstance(opening_record['closed'], bool)):
				error_msg = "opening_record['closed'] must be a boolean.\n"
				error_msg += "opening_record['closed'] is type {}".format(type(opening_record['closed']))

				self.data = {"message": error_msg}
				self.status_code = 400
				location_data_ok = False

				return location_data_ok


		# the opening recod data is valid:
		return True


	


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

		# # convert the ObjectId in the location object:
		record['_id'] = str(record['_id'])


		# Convert Location ObjectIds:
		for l_key, l_value in record.items():
			if isinstance(l_value, ObjectId):
				record[l_key] = str(l_value)


		# convert the ObjectId for each opeing time sub document
		for opening_time in record['openingTimes']:
			for o_key, o_value in opening_time.items():
				if isinstance(o_value, ObjectId):
					opening_time[o_key] = str(o_value) 


		# convert the ObjectId for each review sub document
		# pdb.set_trace()
		for review in record['reviews']:
			for r_key, r_value in review.items():
				if isinstance(r_value, ObjectId):
					review[r_key] = str(r_value)



		return record 


	def build_opening_times(self, opening_times_list):
		'''


		'''

		# add the opening time sub documents:
		opening_time_records = list()
		for opening_time in opening_times_list:

			# add valid opening time:
			if opening_time['closed']:
				opening_record = OpeningTime(
					days=opening_time['days'],
					closed=opening_time['closed']
				)

			else:
				opening_record = OpeningTime(
					days=opening_time['days'],
					opening=opening_time['opening'],
					closing=opening_time['closing'],
					closed=opening_time['closed'] 
					)

			opening_time_records.append(opening_record)


		return opening_time_records

	# def is_object_id_ok(self, request, object_id):
	# 	'''

	# 	Validate object_id is ObjectId object. Any invalid object_id is a 401 error.


	# 	'''

	# 	if not bson.objectid.ObjectId.is_valid(object_id):

	# 		scheme, netloc, path, query, fragment = urlsplit(request.base_url)

	# 		error_msg = "{} {}{} is not valid\n".format(request.method, path, query)
	# 		error_msg += "{} is not a valid id".format(object_id)

	# 		self.data = {'message': error_msg}
	# 		self.status_code = 404

	# 		return False 

	# 	return True


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





	# def get_location_rating(self, location_obj):
	# 	'''


	# 	'''

	# 	rating = 0

	# 	if len(location_obj.reviews) > 0:
	# 		for review in location_obj.reviews:
	# 			rating += review.rating 

	# 		rating /= len(location_obj.reviews)

	# 		rating = int(rating)

	# 	return rating

# End: helper methods:
# *******************************************************************************
