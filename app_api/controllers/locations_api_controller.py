

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

			if self.is_object_id(object_id=location_id):
				self.read_location_by_id(location_id=location_id)

			else:
				# bad object id:
				pass 


		elif (request.method == 'POST') and (location_id is None):
			self.create_location(data=request.get_json())

		
		elif (request.method == 'POST') and (location_id is not None):
			# in valid POST request:
			pass 


		elif (request.method == 'PUT') and (location_id is not None):
			if self.is_object_id(object_id=location_id):
				self.update_location(location_id=location_id, data=request.json())

			else:
				pass 



		elif (request.method == 'PUT') and (location_id is None):
			# invalid PUT request:
			pass 


		elif (request.method == 'DELETE') and (location_id is not None):
			if self.is_object_id(object_id=location_id):
				self.delete_location(location_id=location_id)

			else:
				pass 

		
		elif (request.method == 'DELETE') and (location_id is None):
			# invalid DELETE request:
			pass







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





	def read_locations_by_distance(self):
		'''

		'''
		
		pass  


	def read_location_by_id(self, location_id):
		'''

		'''

		pass 

	def update_location(self, location_id, data):
		'''


		'''

		pass 


	def delete_location(self, location_id):
		'''

		'''
		pass 


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
				location_data_ok = False

				return location_data_ok

		# validate location_data['name']: 
		if (isinstance(location_data['name'], str)):
			if len(location_data['name']) == 0:
				error_msg = "Invalid data for location['name'].\n"
				error_msg += "location['name'] an empty string."

				self.data = {"message": error_msg}
				self.status_code = 400
				location_data_ok = False

				return location_data_ok

		else:
				error_msg = "location['name'] must be a string.\n"
				error_msg += "location['name'] is type {}".format(type(location_data['name']))

				self.data = {"message": error_msg}
				self.status_code = 400
				location_data_ok = False

				return location_data_ok


		# validate location_data['lng']: 
		if (isinstance(location_data['lng'], float)):
			if -180 <= location_data['lng'] <= 180:
				pass

			else:
				error_msg = "Invalid data for location['lng'] = {}.\n".format(location_data['lng'])
				error_msg += "location['lng'] must be between -180 and 180"

				self.data = {"message": error_msg}
				self.status_code = 400
				location_data_ok = False

				return location_data_ok

		else:
				error_msg = "location['lng'] must be a float.\n"
				error_msg += "location['lng'] is type {}".format(type(location_data['lng']))

				self.data = {"message": error_msg}
				self.status_code = 400
				location_data_ok = False

				return location_data_ok

		# validate location_data['lat']: 
		if (isinstance(location_data['lat'], float)):
			if -90 <= location_data['lat'] <= 90:
				pass

			else:
				error_msg = "Invalid data for location['lat'] = {}.\n".format(location_data['lat'])
				error_msg += "location['lat'] must be between -90 and 90"

				self.data = {"message": error_msg}
				self.status_code = 400
				location_data_ok = False

				return location_data_ok

		else:
				error_msg = "location['lat'] must be a float.\n"
				error_msg += "location['lat'] is type {}".format(type(location_data['lat']))

				self.data = {"message": error_msg}
				self.status_code = 400
				location_data_ok = False

				return location_data_ok


		location_data_ok = True
		return location_data_ok



	def is_opening_data_ok(self, opening_data):
		'''

		'''

		pass




# End: helper methods:
# *******************************************************************************
