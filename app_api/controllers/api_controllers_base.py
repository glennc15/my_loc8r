


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


	# End: helper methods:
	# *******************************************************************************











	