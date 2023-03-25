from urllib.parse import urlsplit
import bson
from bson import ObjectId
import re 
import json
import mongoengine as me



from my_loc8r.app_api.models.location_models import Location, OpeningTime, Review

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


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
			self.read_locations_by_distance(request=request)

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

			# 405 and 401 errors:
			#if we made it this far then something is wrong with the request
			
			scheme, netloc, path, query, fragment = urlsplit(request.base_url)

			# 405 errors for route /api/locations. allowed methods = ['GET', 'POST']
			if (re.search(r'/api/locations', path)) and (request.method not in ['GET', 'POST']):
				error_msg = "{} request is not valid for url {}".format(request.method, path)
				self.data = {'message': error_msg}
				self.status_code = 405

				return None

			
			# 405 errors for route /api/locations/:locationid. allowed methods = ['GET', 'PUT', 'DELETE']
			if (re.search(r'/api/locations/[a-f\d]{24}', path, re.I)) and (request.method not in ['GET', 'PUT', 'DELETE']):
				error_msg = "{} request is not valid for url {}".format(request.method, path)
				self.data = {'message': error_msg}
				self.status_code = 405

				return None

			
			# all 401 requests:
			else:
				error_msg = "{} {}{} is not valid. Check the url or the request method".format(request.method, path, query)
				self.data = {'message': error_msg}
				self.status_code = 401

				return None



	# # POST: /api/locations/<locationid>/reviews
	# def create_review(self. request, location_id):
	# 	'''


	# 	'''

	# 	if is_object_id_ok(request=request, object_id=)



	# reviews is going the way of the dodo bird and will be replaced with 1
	# method for each crud operation. Flask will handle all 405 errors (as it
	# should be!)
	# def reviews(self, request, location_id=None, review_id=None):
	# 	'''
		
	# 	acceptable routes:

	# 	1) url = /api/locations/<locationid>/reviews = ['POST']
		
	# 	2) url = /api/locations/<locationid>/reviews/<reviewid>, methods = ['GET', 'PUT', 'DELETE']


	# 	'''

	# 	# scheme, netloc, path, query, fragment = urlsplit(request.base_url)

	# 	# if (path=='/api/locations/reviews') and (request.method=='POST'):
	# 	# 	pdb.set_trace()

	# 	if (request.method == 'POST') and (location_id is not None):
	# 		if self.is_object_id_ok(request=request, object_id=location_id):
	# 			self.create_review(location_id=location_id, new_data=request.get_json())
	# 			return None

	# 	elif (request.method == 'GET') and (location_id is not None) and (review_id is not None):
	# 		if self.is_object_id_ok(request=request, object_id=location_id) and (self.is_object_id_ok(request=request, object_id=review_id)):
	# 			self.read_review(location_id=location_id, review_id=review_id)
	# 			return None

	# 	elif (request.method == 'PUT') and (location_id is not None) and (review_id is not None):
	# 		if self.is_object_id_ok(request=request, object_id=location_id) and (self.is_object_id_ok(request=request, object_id=review_id)):
	# 			self.update_review(location_id=location_id, review_id=review_id, new_data=request.get_json())
	# 			return None

	# 	elif (request.method == 'DELETE') and (location_id is not None) and (review_id is not None):
	# 		if self.is_object_id_ok(request=request, object_id=location_id) and (self.is_object_id_ok(request=request, object_id=review_id)):
	# 			self.delete_review(location_id=location_id, review_id=review_id)
	# 			return None


	# 	else:

	# 		# 405 and 404 errors:
	# 		#if we made it this far then something is wrong with the request
			
	# 		scheme, netloc, path, query, fragment = urlsplit(request.base_url)



	# 		# 405 errors for route /api/locations. allowed methods = ['GET', 'POST']
	# 		if (re.search(r'/api/locations/[a-f\d]{24}/reviews', path)) and (request.method not in ['POST']):
	# 			error_msg = "{} request is not valid for url {}".format(request.method, path)
	# 			self.data = {'message': error_msg}
	# 			self.status_code = 405

	# 			return None

			
	# 		# 405 errors for route /api/locations/:locationid. allowed methods = ['GET', 'PUT', 'DELETE']
	# 		if (re.search(r'/api/locations/[a-f\d]{24}/reviews/[a-f\d]{24}', path, re.I)) and (request.method not in ['GET', 'PUT', 'DELETE']):
	# 			error_msg = "{} request is not valid for url {}".format(request.method, path)
	# 			self.data = {'message': error_msg}
	# 			self.status_code = 405

	# 			return None

			
	# 		# all 404 requests:
	# 		else:
	# 			error_msg = "{} {}{} is not valid. Check the url or the request method".format(request.method, path, query)
	# 			self.data = {'message': error_msg}
	# 			self.status_code = 404

	# 			return None





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




	def read_locations_by_distance(self, request):
		'''

		'''
		
		longitude, latitude, max_dist = self.parse_location_parameters(parameters=request.args)

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


			locations = Location.objects().aggregate(pipeline)

			self.data = [self.format_location(document=x) for x in locations]
			self.status_code = 200


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


	# POST: /api/locations/<locationid>/reviews
	def create_review(self, location_id, review_data):
		'''

 
		'''

		# sometimes review_data['reviewData'] exists, convert it to review_data['review_text']
		if review_data.get('reviewText'):
			review_data['review_text'] = review_data['reviewText']

		# remove any unnessary fields from review_data:
		review_data = dict([(k, v) for k, v in review_data.items() if k in ['author', 'rating', 'review_text']])

		# Build a Review model using review_data and validate:
		review = Review(**review_data)

		try:
			review.validate()

		except Exception as e:
			if isinstance(e, me.errors.ValidationError):
				self.status_code = 400
				self.data = {'error': e.message}
				return None 

			else:
				raise e 


		# Get the location:
		try:
			location = Location.objects(id=location_id).get()

		except Exception as e:
			if isinstance(e, me.errors.ValidationError):
				self.status_code = 404
				self.data = {'error': e.message}
				return None 

			else:
				raise e 


		# add the review to the location:
		location.reviews.append(review)
		location.rating = self.get_location_rating(location_obj=location)

		try: 
			location.save()

		except Exception as e:
			print("500 Error!!!")
			raise e 


		# convert review._id to a string before sending the response:
		review_dict = review.to_mongo().to_dict()
		review_dict['_id'] = str(review_dict['_id'])

		self.data = review_dict
		self.status_code = 201

	# GET: /api/locations/<locationid>/reviews/<reviewid>
	def read_review(self, location_id, review_id):
		'''

		# 12Mar23: I cannot come up with a query to return just a review that matches review_id.
		
		These queryies all return a Location:
		location = Location.objects(id=location_id).get()
		location = Location.objects(id=location_id, reviews__review_id=review).get()
		location = Location.objects(reviews__review_id=review).get()

		I've also tried .only('reviews') but still returns a Location.

		So finding the review in the location manually until I have more knowledge to build a better query.

		'''

		try:
			# location = Location.objects(id=location_id).get()
			# location = Location.objects(=review_id).get()
			location = Location.objects(__raw__={'_id': ObjectId(location_id), 'reviews._id': ObjectId(review_id)}).get()

			print("location_id = {}".format(location_id))
			print("review_id = {}".format(review_id))
			print("location = {}".format(location))


			# pdb.set_trace()


		except Exception as e:
			if isinstance(e, me.errors.ValidationError):
				self.status_code = 404
				self.data = {'error': e.message}
				return None

			elif isinstance(e, Location.DoesNotExist):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			elif isinstance(e, bson.errors.InvalidId):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			else:
				raise e 


		# get the right review:
		target_review = [x for x in location.reviews if x._id == ObjectId(review_id)][0].to_mongo().to_dict()
		target_review['_id'] = str(target_review['_id'])

		self.status_code = 200
		self.data = target_review





		# 	# print("Exception = {}".format(e))

		# 	# error_msg = "No location record with id = {} found.".format(location_id)
		# 	# self.data = {'message': error_msg}
		# 	# self.status_code = 404

		# 	# return None

		# location_data = self.format_location(document=location)
		# # location_data = location.to_mongo().to_dict()		
		# # print("location_data = {}".format(location_data))

		# target_review = [x for x in location_data['reviews'] if x['review_id']==review_id]

		# if len(target_review) == 1:
		# 	self.data = target_review[0]
		# 	self.status_code = 200

		# else:
		# 	error_msg = "No reveiw record with id = {} found.".format(review_id)
		# 	self.data = {'message': error_msg}
		# 	self.status_code = 404





	# def read_review(self, location_id, review_id):
	# 	'''

	# 	# 12Mar23: I cannot come up with a query to return just a review that matches review_id.
		
	# 	These queryies all return a Location:
	# 	location = Location.objects(id=location_id).get()
	# 	location = Location.objects(id=location_id, reviews__review_id=review).get()
	# 	location = Location.objects(reviews__review_id=review).get()

	# 	I've also tried .only('reviews') but still returns a Location.

	# 	So finding the review in the location manually until I have more knowledge to build a better query.

	# 	'''
	# 	try:
	# 		location = Location.objects(id=location_id).get()

	# 		# location = Location.objects()

	# 	except Exception as e:

	# 		print("Exception = {}".format(e))

	# 		error_msg = "No location record with id = {} found.".format(location_id)
	# 		self.data = {'message': error_msg}
	# 		self.status_code = 404

	# 		return None

	# 	location_data = self.format_location(document=location)
	# 	# location_data = location.to_mongo().to_dict()		
	# 	# print("location_data = {}".format(location_data))

	# 	target_review = [x for x in location_data['reviews'] if x['review_id']==review_id]

	# 	if len(target_review) == 1:
	# 		self.data = target_review[0]
	# 		self.status_code = 200

	# 	else:
	# 		error_msg = "No reveiw record with id = {} found.".format(review_id)
	# 		self.data = {'message': error_msg}
	# 		self.status_code = 404


	def update_review(self, location_id, review_id, new_data):
		'''


		'''
		# Question.objects(id="question_id", answers__uid="uid").update(set__answers__S__answer__status="new_status")

		# Validate the review data:

		if not self.is_review_data_ok(review_data=new_data):
			# the review data is invalid so exit:
			return None 

		raw_set_query = {
			'$set': {
				'reviews.$.author': new_data['author'],
				'reviews.$.rating': new_data['rating'], 
				'reviews.$.review_text': new_data['reviewText'], 

			}
		}

		# # Verify the location exits:
		# try:
		# 	location = Location.objects(id=location_id).get()

		# except Exception as e:

		# 	print('Exception e = {}'.format(e))

		# 	error_msg = "No location record with id = {} found.".format(location_id)
		# 	self.data = {'message': error_msg}
		# 	self.status_code = 404

		# 	return None


		# Find the location and review exits:
		try:
			location = Location.objects(id=location_id, reviews__review_id=review_id).get()

		except Exception as e:

			print('Exception e = {}'.format(e))

			error_msg = "No location with _id = {}, and review _id = {} found.".format(location_id, review_id)
			self.data = {'message': error_msg}
			self.status_code = 404

			return None


		location = Location.objects(id=location_id, reviews__review_id=review_id).update(__raw__=raw_set_query)

		if location == 1:
			# update the location review:
			location = Location.objects(id=location_id).get()
			location.rating = self.get_location_rating(location_obj=location)
			location.save()


			self.read_review(location_id=location_id, review_id=review_id)	


		else:
			raise ValueError("Problem with update review!")





	def delete_review(self, location_id, review_id):
		'''


		'''


		# db.collection.update({ d : 2014001 , m :123456789},
        #               {$pull : { "topups.data" : {"val":NumberLong(200)} } } )



		# Find the location and review exits:
		try:
			location = Location.objects(id=location_id, reviews__review_id=review_id).get()

		except Exception as e:

			print('Exception e = {}'.format(e))

			error_msg = "No location with _id = {}, and review _id = {} found.".format(location_id, review_id)
			self.data = {'message': error_msg}
			self.status_code = 404

			return None

		# removing the review manually because I cannot get the $pull update to work properly

		location.reviews = [x for x in location.reviews if str(x.review_id) != review_id]
		location.rating = self.get_location_rating(location_obj=location)
		location.save()

		self.data = {'message': "deleted review with id = {}".format(review_id)}
		self.status_code = 204


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

	def is_latitude_ok(self, latitude):
		'''


		'''

		# validate location_data['lat']: 
		if (isinstance(latitude, float)):
			if -90 <= latitude <= 90:
				pass

			else:
				error_msg = "Invalid data for location['lat'] = {}.\n".format(latitude)
				error_msg += "location['lat'] must be between -90 and 90"

				self.data = {"message": error_msg}
				self.status_code = 404

				return False

		else:
				error_msg = "location['lat'] must be a float.\n"
				error_msg += "location['lat'] is type {}".format(type(latitude))

				self.data = {"message": error_msg}
				self.status_code = 404

				return False


		return True


	def is_longitude_ok(self, longitude):
		'''

		'''
		# validate location_data['lng']: 
		if (isinstance(longitude, float)):
			if -180 <= longitude <= 180:
				pass

			else:
				error_msg = "Invalid data for location['lng'] = {}.\n".format(longitude)
				error_msg += "location['lng'] must be between -180 and 180"

				self.data = {"message": error_msg}
				self.status_code = 404

				return False

		else:
				error_msg = "location['lng'] must be a float.\n"
				error_msg += "location['lng'] is type {}".format(type(longitude))

				self.data = {"message": error_msg}
				self.status_code = 404

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


	def is_review_data_ok(self, review_data):

		'''
		 
		checks review_data contains the required fields:

		'''

		review_data_ok = True
		error_dict = dict()

		# check all required keys are in review_data:
		for required_key in self._required_review_keys:
			if required_key not in review_data.keys():
				error_dict[required_key] = "{} field is required".format(required_key)
				review_data_ok = False


		if review_data_ok == False:
			self.status_code = 400
			self.data = error_dict


		return review_data_ok

		# review = Review(
		# 	author=review_data['author'],
		# 	rating=review_data['rating'],
		# 	review_text=review_data['reviewText']
		# )

		# validate each field in review_data using the  



	# def is_review_data_ok(self, review_data):
	# 	'''


	# 	'''

	# 	# check review_data is a dict:
	# 	if not isinstance(review_data, dict):
	# 		error_msg = "Invalid type for a review record.\n"
	# 		error_msg += "This review record is of type {}".format(type(opening_record))

	# 		self.data = {"message": error_msg}
	# 		self.status_code = 400

	# 		return False


	# 	# check review_data for the required values:
	# 	for review_key in self._required_review_keys:
	# 		if review_key not in review_data:
	# 			error_msg = "Invalid data for this review.\n"
	# 			error_msg += "review['{}'] is required.".format(review_key)

	# 			self.data = {"message": error_msg}
	# 			self.status_code = 400

	# 			return False

	# 	# validate review_data['author']: 
	# 	if (isinstance(review_data['author'], str)):
	# 		if len(review_data['author']) == 0:
	# 			error_msg = "Invalid data for review['author'].\n"
	# 			error_msg += "review['author'] an empty string."

	# 			self.data = {"message": error_msg}
	# 			self.status_code = 400

	# 			return False

	# 	else:
	# 			error_msg = "review['author'] must be a string.\n"
	# 			error_msg += "review['author'] is type {}".format(type(review_data['author']))

	# 			self.data = {"message": error_msg}
	# 			self.status_code = 400
	# 			location_data_ok = False

	# 			return location_data_ok

	# 	# validate review_data['reviewText']: 
	# 	if (isinstance(review_data['reviewText'], str)):
	# 		if len(review_data['reviewText']) == 0:
	# 			error_msg = "Invalid data for review['reviewText'].\n"
	# 			error_msg += "review['reviewText'] an empty string."

	# 			self.data = {"message": error_msg}
	# 			self.status_code = 400

	# 			return False

	# 	else:
	# 			error_msg = "review['reviewText'] must be a string.\n"
	# 			error_msg += "review['reviewText'] is type {}".format(type(review_data['reviewText']))

	# 			self.data = {"message": error_msg}
	# 			self.status_code = 400
	# 			location_data_ok = False

	# 			return location_data_ok

	# 	# validate review_data['rating']: 
	# 	if not (isinstance(review_data['rating'], int)):
	# 			error_msg = "review['rating'] must be a int.\n"
	# 			error_msg += "review['rating'] is type {}".format(type(review_data['rating']))

	# 			self.data = {"message": error_msg}
	# 			self.status_code = 400
	# 			location_data_ok = False

	# 			return location_data_ok


	# 	# the review data is valid:
	# 	return True	


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

		# convert the ObjectId for each opeing time sub document
		for opening_time in record['openingTimes']:
			opening_time['_id'] = str(opening_time['_id'])

		# convert the ObjectId for each review sub document
		# pdb.set_trace()
		for review in record['reviews']:
			print("review.keys() = {}".format(review.keys()))

			if review.get('review_id'):
				review['review_id'] = str(review['review_id'])

			else:
				review['_id'] = str(review['_id'])

			# review['_id'] = str(review['_id'])


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
			self.status_code = 404

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
