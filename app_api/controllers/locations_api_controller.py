from urllib.parse import urlsplit
import bson
from bson import ObjectId
import re 
import json
import mongoengine as me


from my_loc8r.app_api.controllers.api_controllers_base import APIControllersBase
from my_loc8r.app_api.models.location_models import Locations, OpeningTime
from my_loc8r.app_api.controllers.locations_generator.generate_locations import GenerateLocations


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


		
		# validating the longitude and latitude with a location model instance. all parameters are strings so must be converted to floats
		try:
			Locations(
				name='abc',
				address='123',
				coords=[float(parameters['lng']), float(parameters['lat'])]
				).validate()

		except Exception as e:
			self.common_validation_errors(e)
			return None 

		
		start_point = {
			'type': 'Point',
			'coordinates': [float(parameters['lng']), float(parameters['lat'])]

		}


		if parameters.get('maxDistance'):

			# max_dist is in km. Must be converted to m:
			max_dist_m = float(parameters['maxDistance']) * 1000

		else:
			max_dist_m = 10000 * 1000

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


		try:
			# pdb.set_trace()

			locations = Locations.objects().aggregate(pipeline)

		except Exception as e:
			self.common_validation_errors(e)
			return None

		
		self.data = [self.format_location(document=x) for x in locations]
		self.status_code = 200


		# there should always be some locations. If there are less than 5
		# locations then generate more and add them to the database:
		if len(self.data) < 5:
			GenerateLocations(
				origin_longitude=float(parameters['lng']),
				origin_latitude=float(parameters['lat']),
				max_dist=float(parameters['maxDistance']),
				n=10, 
				existing_locations=[x['name'] for x in self.data],
				location_ctrl_obj=LocationsAPIController()
			)

			# pdb.set_trace()
			
			# read the new locations from the database:
			self.read_locations_by_distance(parameters=parameters)


	# GET:/api/locations/<locationid>
	def read_location_by_id(self, location_id):
		'''
		
		15April23: adding reviews.author_reviews which is the total number of
		reviews by the author. Achieveing this with an aggregation pipeline.

		'''


		# the aggregation pipeline will return and empty list if the location
		# does not have any reviews.  So caryying out he query in 2 steps:

		# 1) make a regular match query. This does 2 things: tiggers a 404 if
		# location_id is not in the database. And also makes it easier to
		# update .views counter. 

		# 2) call the location with the aggregation pipeline. If the pipeline is successful
		# then it will return the location with the proper .views counter and
		# the new reviews.author_reviews. If the pipeline returns an empty
		# list then the issue is the location does not have any reviews so
		# return the locaiton from the first query.

		# first query of the location:
		try:
			location = Locations.objects(id=location_id).get()

		except Exception as e:
			self.common_validation_errors(e)
			return None 

		location.views += 1
		location.save() 


		# second query of the location using an aggregation pipeline:
		pipeline = [
			# find the location by id:
			{
				'$match': {
					'_id': ObjectId(location_id)
				}
			},
			# create a separate record for each review. This allows adding
			# author data for each review author:
			{
				'$unwind': '$reviews'
			},
			# add user data for each review author:
			{
				'$lookup': {
					'from': 'users',
					'localField': 'reviews.author_id',
					'foreignField': '_id',
					'as': 'author_data'
				}
			},
			# now can calculate .author_reviews with is length of
			# users.reviews_created. Have to do this in 2 steps:
			
			# author data is a 1 element array of an array. This first step
			# converters to a single array
			{
				'$set': {
					'author_data': {'$first': '$author_data'}
				}
			},
			# calculate reviews.author_reviews:
			{
				'$set': {
					'reviews.author_reviews': {'$size': '$author_data.reviews_created'}
				}
			},
			# combine all the records back into 1 document:
			{
				'$group': {
					'_id': {
						'_id': '$_id',
						'name': '$name',
						'address': '$address',
						'rating': '$rating',
						'facilities': '$facilities',
						'coords': '$coords',
						'openingTimes': '$openingTimes',
						'views': '$views',

					},
					'reviews': {'$push': '$reviews'}
				}
			},
			# final cleanup:
			{
				'$project': {
					'_id': '$_id._id',
					'name': '$_id.name',
					'address': '$_id.address',
					'rating': '$_id.rating',
					'facilities': '$_id.facilities',
					'coords': '$_id.coords',
					'openingTimes': '$_id.openingTimes',
					'views': '$_id.views',
					'reviews': 1,
				}
			}

		]

		locations = list(Locations.objects().aggregate(pipeline))

		# This is a location with reviews and the new reviews.author_reviews:
		if len(locations) == 1:
			self.data = self.format_location(document=locations[0])
			self.status_code = 200

		# The location doesn't have any reviews so use the first query result:
		elif len(locations) == 0:
			self.data = self.format_location(document=location)
			self.status_code = 200

		# hope we never get here:
		else:
			raise ValueError("read_location_by_id(location_id={})".format(location_id))


	# PUT:/api/locations/<locationid>
	def update_location(self, location_id, location_data):
		'''




		'''

		# remove any excess keys from location_data:
		update_data = dict([(k,v) for k,v in location_data.items() if k in ['name', 'address', 'rating', 'facilities']])		

		# add location coordinates if they are included in location_data:
		if location_data.get('lng') and location_data.get('lat'):
			update_data['coords'] = [location_data['lng'], location_data['lat']]

		try:
			location = Locations.objects(id=location_id).get().update(**update_data)

		except Exception as e:
			self.common_validation_errors(e)
			return None 

		self.read_location_by_id(location_id=location_id)




	# DELETE:/api/locations/<locationid>
	def delete_location(self, location_id):
		'''

		'''

		try:
			location = Locations.objects(id=location_id).get().delete()

		except Exception as e:	
			self.common_validation_errors(e)
			return None 


		self.data = {'message': "location with id = {} was successfully removed".format(location_id)}
		self.status_code = 204



	# End: Public methods:
	# *******************************************************************************








