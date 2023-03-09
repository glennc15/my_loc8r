from urllib.parse import urlsplit
import bson

from my_loc8r.app_api.models.location_models import Location, OpeningTime, Review

class LocationsAPIController(object):
	'''
	
	Controller class for all API routes.

	'''

	def __init__(self):
		'''

		'''

		self.status_code = None 
		self.data = None


		self._required_location_keys = ['name', 'lng', 'lat']
		self._required_opening_keys = ['closed', 'days']
		self._required_review_keys = ['author', 'rating', 'reviewText']





# *******************************************************************************
# START: Public methods:


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


	def locations(self, request, location_id=None):
		'''
		
		acceptable routes:

		1) url = /api/locations, methods = ['GET', 'POST']
		
		2) url = /api/locations/locationid, methods = ['GET', 'PUT', 'DELETE']


		'''

		if (request.method == 'GET') and (location_id is None):
			self.read_locations_by_distance()

		elif (request.method == 'GET') and (location_id is not None):

			if self.is_object_id_ok(request=request, object_id=location_id):
				self.read_location_by_id(location_id=location_id)

			else:
				# problem with location_id:
				return False 


		elif (request.method == 'POST') and (location_id is None):
			self.create_location(data=request.get_json())

		
		# elif (request.method == 'POST') and (location_id is not None):
		# 	# in valid POST request:
		# 	pass 


		elif (request.method == 'PUT') and (location_id is not None):
			if self.is_object_id_ok(request=request, object_id=location_id):
				self.update_location(location_id=location_id, new_data=request.get_json())

			else:
				# location_id is invalid:
				return False 



		# elif (request.method == 'PUT') and (location_id is None):
		# 	# invalid PUT request:
		# 	pass 


		elif (request.method == 'DELETE') and (location_id is not None):
			if self.is_object_id_ok(request=request, object_id=location_id):
				self.delete_location(location_id=location_id)
				
			else:
				# location_id is invalid:
				return False 

		
		# elif (request.method == 'DELETE') and (location_id is None):
		# 	# invalid DELETE request:
		# 	pass

		else:
			# all 401 requests:

			scheme, netloc, path, query, fragment = urlsplit(request.base_url)

			error_msg = "{} {}{} is not valid. Check the url or the request method".format(request.method, path, query)

			# print('error_msg = {}'.format(error_msg))

			self.data = {'message': error_msg}
			self.status_code = 401

			return None







	def reviews(self, request, location_id=None, reviewid=None):
		'''


		'''

		pass



# End: Public methods:
# *******************************************************************************


# *******************************************************************************
# START: helper methods:
	
	def create_location(self, data):
		'''

		'''
		
		if not self.is_location_data_ok(location_data=data):
			# there is a problem with the location data so exit:
			return None

		if not self.is_opening_data_ok(opening_data=data['openingTimes']):
			# there is a problem with the opening data so exit:
			return None


		location = Location(
			name=data['name'],
			address=data['address'],
			facilities=data['facilities'],
			coords = [data['lng'], data['lat']]
		)

		opening_time_records = self.build_opening_times(opening_times_list=data['openingTimes'])
		location.openingTimes = opening_time_records

		try:
			location.save()

			# remove the ObjectId objects:
			location_data = self.convert_object_ids(document=location)

			self.data = location_data
			self.status_code = 201

			# successful POST so exit
			return None

		except Exception as e:
			# not sure how to test this

			print("500 Error!")
			print(e)

			self.data = {'message': 'database error!'}
			self.status_code = 500

			return None 




	def read_locations_by_distance(self):
		'''

		'''
		
		pass  


	def read_location_by_id(self, location_id):
		'''

		'''

		try:

			location = Location.objects(id=location_id).get()
			
			location_data = self.format_location(document=location)

			self.data = location_data
			self.status_code = 200
	

		except Exception as e:

			error_msg = "No location record with id = {} found.".format(location_id)
			self.data = {'message': error_msg}
			self.status_code = 404
			




	def update_location(self, location_id, new_data):
		'''


		'''
		# Find the location by id:
		try:
			location = Location.objects(id=location_id).get()

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


	def delete_location(self, location_id):
		'''

		'''

		try:
			location = Location.objects(id=location_id).get().delete()
			self.data = {'message': "location with id = {} was successfully removed".format(location_id)}
			self.status_code = 204

		except Exception as e:
			# not sure how to test this
			print("500 Error!")
			print(e)

			self.data = {'message': 'database error!'}
			self.status_code = 500

		return None 


	def is_object_id(self, object_id):
		'''


		'''

		pass 

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

		record = document.to_mongo().to_dict()

		# # convert the ObjectId in the location object:
		record['_id'] = str(record['_id'])

		# convert the ObjectId for each opeing time sub document
		for opening_time in record['openingTimes']:
			opening_time['_id'] = str(opening_time['_id'])

		# convert the ObjectId for each review sub document
		for review in record['reviews']:
			review['_id'] = str(review['_id'])


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

	def is_object_id_ok(self, request, object_id):
		'''

		Validate object_id is ObjectId object. Any invalid object_id is a 401 error.


		'''

		if not bson.objectid.ObjectId.is_valid(object_id):

			scheme, netloc, path, query, fragment = urlsplit(request.base_url)

			error_msg = "{} {}{} is not valid\n".format(request.method, path, query)
			error_msg += "{} is not a valid id".format(object_id)

			self.data = {'message': error_msg}
			self.status_code = 401

			return False 

		return True


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

# End: helper methods:
# *******************************************************************************
