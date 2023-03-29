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




	# def format_location(self, document):
	# 	'''


	# 	'''
	# 	# remove the object ids:
	# 	location_data =  self.convert_object_ids(document=document)

	# 	# seperate 'coords' into longatude and lattitude and then remove 'coords'
	# 	location_data['lng'] = location_data['coords']['coordinates'][0]
	# 	location_data['lat'] = location_data['coords']['coordinates'][1]

	# 	# remove coords from dictionary:
	# 	location_data = dict([(k, v) for k, v in location_data.items() if k not in ['coords']])


	# 	return location_data





# End: helper methods:
# *******************************************************************************
