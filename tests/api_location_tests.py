import unittest
from bson import ObjectId
from urllib.parse import urlsplit, urlunsplit

from pymongo import MongoClient
import pymongo

# import collections

import datetime
import time 

# import tzlocal
# import pytz

import requests

import jwt
from dotenv import load_dotenv
import os

# from my_loc8r.app_api.models.user_model import Users
# # from ..components.mongo_repository import MongoRepository
# from components.mongo_repository import MongoRepository
# from components.mongo_records_reader import MongoRecordsReader 

from api_endpoint_testing import APIEndPointTests, endpoint_test

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class APILocationTests(unittest.TestCase):

	mongo_address = "mongodb://192.168.1.2:27017"
	mongo_client = MongoClient(mongo_address)


	@classmethod
	def setUpClass(cls):
		'''

		'''

		load_dotenv()
		cls._encode_key = os.environ.get('JWT_SECRETE')


	@classmethod
	def tearDownClass(cls):
		''' 


		'''

		APILocationTests.mongo_client.close()



	def setUp(self):
		'''


		'''
		self.scheme = 'http'
		self.url = '127.0.0.1:5000'
		self.db_name = 'myLoc8r'

		# self.url = 'localhost:3000'


	# POST:/api/locations
	def test_location_create_01(self):
		'''


		'''

		self.reset_locations_collection()

		# CREATE unsuccessful: due to an invalid url:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', str(ObjectId())]), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=405, 
			descriptive_error_msg="invalid method for endpoint"
		)


		# CREATE unsuccessful: due to missing name field (required):
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="name is required"
		)


		# CREATE unsuccessful: due to missing invalid name field (required):
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': '',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="name is an empty string"
		)



		# CREATE unsuccessful: due to missing longitude coordinate (required):
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="longitude is required"
		)



		# CREATE unsuccessful: due to invalid longitude coordinate:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -180.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="longitude is invalid"
		)


		# CREATE unsuccessful: due to invalid longitude coordinate:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': 180.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="longitude is invalid"
		)


		# CREATE unsuccessful: due to missing latitude coordinates (required):
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="lattitue is required"
		)


		# CREATE unsuccessful: due to invalid latitude coordinate:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 90.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="lattitue is invalid"
		)

		# CREATE unsuccessful: due to invalid latitude coordinate:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': -90.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="lattitue is invalid"
		)



		# a successful POST:
		location_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
			}, 
			auth=None, 
			expected_status_code=201, 
			descriptive_error_msg="create location success"
		)

		self.assertIsInstance(ObjectId(location_r.json()['_id']), ObjectId)
		self.assertEqual(location_r.json()['name'], 'Burger QueEn')
		self.assertEqual(location_r.json()['address'], '783 High Street, Reading, RG6 1PS')
		self.assertEqual(location_r.json()['facilities'], 'Food,Premium wifi')
		self.assertEqual(location_r.json()['rating'], 0)
		self.assertEqual(location_r.json()['lng'], -0.9690854)
		self.assertEqual(location_r.json()['lat'], 51.455051)
		self.assertEqual(len(location_r.json()['openingTimes']), 0)
		self.assertEqual(len(location_r.json()['reviews']), 0)



		# CREATE unsuccessful: due to invalid openingTimes record:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="invalid opeing time record"
		)


		# CREATE unsuccessful: due to missing openingTimes['days']:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="invalid opening time record"
		)



		# CREATE unsuccessful: due to invalid openingTimes['days']:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': 5,
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="invalid opening time record"
		)


		# CREATE unsuccessful: due to missing openingTimes['closed']:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="invalid opening time record"
		)


		# invalid test. openingTimes['closed'] = string; openingTimes
		# ['closed'] is expected to be a boolean. But mongoengine will
		# convert a string to a value of True.

		# # CREATE unsuccessful: due to invalid openingTimes['closed']:
		# endpoint_test(
		# 	method='POST', 
		# 	scheme=self.scheme, 
		# 	url=self.url, 
		# 	endpoint='/'.join(['api', 'locations']), 
		# 	data={
		# 		'name': 'Burger QueEn',		
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': 'true'
		# 			}
		# 		]
		# 	}, 
		# 	auth=None, 
		# 	expected_status_code=400, 
		# 	descriptive_error_msg="invalid method for endpoint"
		# )


		# CREATE unsuccessful: due to missing opening field:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="invalid method for endpoint"
		)


		# a successful POST:
		location_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}, 
			auth=None, 
			expected_status_code=201, 
			descriptive_error_msg="successful post"
		)

		self.assertTrue(isinstance(ObjectId(location_r.json()['_id']), ObjectId))
		self.assertEqual(location_r.json()['name'], 'Burger QueEn')
		self.assertEqual(location_r.json()['address'], '783 High Street, Reading, RG6 1PS')
		self.assertEqual(location_r.json()['facilities'], 'Food,Premium wifi')
		self.assertEqual(location_r.json()['lng'], -0.9690854)
		self.assertEqual(location_r.json()['lat'], 51.455051)

		self.assertEqual(location_r.json()['openingTimes'][0]['days'], "Thursday - Saturday")
		self.assertEqual(location_r.json()['openingTimes'][0]['opening'], "1:00am")
		self.assertEqual(location_r.json()['openingTimes'][0]['closing'], "10:00am")
		self.assertFalse(location_r.json()['openingTimes'][0]['closed'])

		self.assertEqual(location_r.json()['openingTimes'][1]['days'], "Monday - Wednesday")
		self.assertTrue(location_r.json()['openingTimes'][1]['closed'])




	def test_location_read_01(self):
		'''


		'''

		location_id = self.add_test_location(reviews=0)

		# common endpoint faiulre tests. Does not do any data validation tests:
		APIEndPointTests(
			scheme=self.scheme,
			url=self.url,
			method='GET',
			endpoint='api/locations/<parentid>',
			auth=None,
			decode_key=None,
			parent_id=location_id,
			child_id=None,
			data=None
		).parent_id_endpoint_tests()

		# READ failure: incorrect method:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data=None, 
			auth=None, 
			expected_status_code=405, 
			descriptive_error_msg="invalid method for endpoint"
		)

		# READ success:
		read1_r = endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data=None, 
			auth=None, 
			expected_status_code=200, 
			descriptive_error_msg="read success"
		)

		self.assertEqual(read1_r.json()['_id'], location_id)
		self.assertEqual(read1_r.json()['name'], 'Burger Queen')
		self.assertEqual(read1_r.json()['address'], '783 High Street, Reading, RG6 1PS')
		self.assertEqual(read1_r.json()['facilities'], 'Food,Premium wifi')
		self.assertEqual(read1_r.json()['rating'], 0)
		self.assertEqual(read1_r.json()['lng'], -0.9690854)
		self.assertEqual(read1_r.json()['lat'], 51.455051)
		self.assertEqual(len(read1_r.json()['openingTimes']), 2)
		self.assertEqual(len(read1_r.json()['reviews']), 0)



	def test_location_crud_01(self):
		'''

		

		'''
		# # CREATE a location:

		# # unsuccessful POST due to an invalid url:
		# url = self.build_url(path_parts=['api', 'locations', '6408d7ef69d46dd24edd9287'])

		# location_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger QueEn',		
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': True
		# 			}
		# 		]
		# 	}
		# )

		# self.assertEqual(location_r.status_code, 405)


		# url = self.build_url(path_parts=['api', 'locations'])
		
		# # unsuccessful POST due to missing name field (required):
		# r = requests.post(
		# 	url=url,
		# 	json={
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': True
		# 			}
		# 		]
		# 	}
		# )

		# # print(r.json())

		# self.assertEqual(r.status_code, 400)


		# # unsuccessful POST due to missing invalid name field (required):
		# r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': '',
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': True
		# 			}
		# 		]
		# 	}
		# )

		# # print(r.json())

		# self.assertEqual(r.status_code, 400)



		# # unsuccessful POST due to missing longitude coordinate (required):
		# r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger Queen',
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': True
		# 			}
		# 		]
		# 	}
		# )

		# self.assertEqual(r.status_code, 400)

		# # unsuccessful POST due to invalid longitude coordinate (required):
		# r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger Queen',
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -180.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': True
		# 			}
		# 		]
		# 	}
		# )

		# # print(r.json())

		# self.assertEqual(r.status_code, 400)

		# # unsuccessful POST due to missing latitude coordinates (required):
		# r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger Queen',
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': True
		# 			}
		# 		]
		# 	}
		# )

		# self.assertEqual(r.status_code, 400)

		# # unsuccessful POST due to invalid latitude coordinate (required):
		# r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger Queen',
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 151.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': True
		# 			}
		# 		]
		# 	}
		# )

		# self.assertEqual(r.status_code, 400)

		# # unsuccessful POST due to invalid openingTimes record:
		# location_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger QueEn',		
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
					
		# 			"Monday - Wednesday",
	
		# 		]
		# 	}
		# )

		# self.assertEqual(r.status_code, 400)

		# # unsuccessful POST due to missing openingTimes['days']:
		# location_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger QueEn',		
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': True
		# 			}
		# 		]
		# 	}
		# )

		# self.assertEqual(r.status_code, 400)

		# # unsuccessful POST due to invalid openingTimes['days']:
		# location_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger QueEn',		
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': 5,
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': True
		# 			}
		# 		]
		# 	}
		# )

		# self.assertEqual(r.status_code, 400)

		# # unsuccessful POST due to missing openingTimes['closed']:
		# location_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger QueEn',		
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 			}
		# 		]
		# 	}
		# )

		# self.assertEqual(r.status_code, 400)

		# # unsuccessful POST due to invalid openingTimes['closed']:
		# location_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger QueEn',		
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': 'True'
		# 			}
		# 		]
		# 	}
		# )

		# self.assertEqual(r.status_code, 400)


		# # a successful POST:
		# location_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger QueEn',		
		# 		'address': "783 High Street, Reading, RG6 1PS",
		# 		'facilities': "Food,Premium wifi",
		# 		'lng': -0.9690854,
		# 		'lat': 51.455051,
		# 		'openingTimes': [
		# 			{
		# 				'days': "Thursday - Saturday",
		# 				'opening': "1:00am",
		# 				'closing': "10:00am",
		# 				'closed': False
		# 			},
		# 			{
		# 				'days': "Monday - Wednesday",
		# 				'closed': True
		# 			}
		# 		]
		# 	}
		# )

		# self.assertEqual(location_r.status_code, 201)
		# self.assertEqual(location_r.json()['name'], 'Burger QueEn')


		# # READ a location:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id']])
		# r = requests.get(url=url)

		# self.assertEqual(r.status_code, 200)
		# self.assertEqual(r.json()['_id'], location_r.json()['_id'])


		# # READ error due to invalid id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:]])
		# r = requests.get(url=url)

		# self.assertEqual(r.status_code, 404)


		# # READ error due to a non existing id:
		# url = self.build_url(path_parts=['api', 'locations', '6408d79c0ba5040bf57d2311'])
		# r = requests.get(url=url)

		# self.assertEqual(r.status_code, 404)


		# # read error due to no id:
		# url = self.build_url(path_parts=['api', 'locations'])
		# r = requests.get(url=url)

		# self.assertEqual(r.status_code, 404)


		# UPDATE a location:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id']])
		location_r = requests.put(
			url=url,
			json={
				'name': 'Burger Queen',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}
		)

		# print("location_r.json() = {}".format(location_r.json()))

		self.assertEqual(location_r.status_code, 200)
		self.assertEqual(location_r.json()['name'], 'Burger Queen')


		# unsuccessful update, invalid id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:]])
		r = requests.put(
			url=url,
			json={
				'name': 'Burger Queen',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}
		)

		self.assertEqual(r.status_code, 404)

		# unsuccessful update, id does not exists:
		url = self.build_url(path_parts=['api', 'locations', '6408d79c0ba5040bf57d2311'])
		r = requests.put(
			url=url,
			json={
				'name': 'Burger Queen',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}
		)

		# print("location_r.json() = {}".format(location_r.json()))

		self.assertEqual(r.status_code, 404)

		# unsuccessful update, no id:
		url = self.build_url(path_parts=['api', 'locations'])
		r = requests.put(
			url=url,
			json={
				'name': 'Burger Queen',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}
		)

		self.assertEqual(r.status_code, 405)


		# DELETE a location:

		# unsuccessful delete, incorrect id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:]])
		r = requests.delete(url=url)
		self.assertEqual(r.status_code, 404)


		# unsuccessful delete, no id:
		url = self.build_url(path_parts=['api', 'locations'])
		r = requests.delete(url=url)
		self.assertEqual(r.status_code, 405)


		# successful delete:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id']])
		r = requests.delete(url=url)
		self.assertEqual(r.status_code, 204)

		

		# 405 Errors: Wrong request methods for a url.

		# unsuccessful PUT due to an invalid url:
		location_r = requests.put(
			url=self.build_url(path_parts=['api', 'locations']),
			json={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}
		)

		self.assertEqual(location_r.status_code, 405)

		# unsuccessful DELETE due to an invalid url:
		location_r = requests.delete(
			url=self.build_url(path_parts=['api', 'locations'])
		)

		self.assertEqual(location_r.status_code, 405)


		# unsuccessful POST due to an invalid url:
		location_r = requests.post(
			url=self.build_url(path_parts=['api', 'locations', '6408d7ef69d46dd24edd9287']),
			json={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}
		)

		self.assertEqual(location_r.status_code, 405)




	def test_locations_geoNear_01(self):
		'''


		'''

		# self.drop_db()
		self.remove_all_records()

		# Set up: build some test locations:
		test_locations = self.build_test_locations()

		url = self.build_url(path_parts=['api', 'locations'])

		# READ: failure with no lattitue parameter
		location_r = requests.get(
			url=url,
			params={
				'lng': -0.9690854,
				'maxDistance': 1
			}
		)

		self.assertEqual(location_r.status_code, 404)



		# READ: failure with no longiture parameter
		location_r = requests.get(
			url=url,
			params={
				'lat': 51.455051,
				'maxDistance': 1
			}
		)

		self.assertEqual(location_r.status_code, 404)

		# READ: failure with invalide longiture parameter
		location_r = requests.get(
			url=url,
			params={
				'lng': -180.9690854,
				'lat': 51.455051,
			}
		)

		self.assertEqual(location_r.status_code, 404)


		# READ: failure with invalide latitude parameter
		location_r = requests.get(
			url=url,
			params={
				'lng': -0.9690854,
				'lat': 151.455051,
			}
		)

		self.assertEqual(location_r.status_code, 404)


		# READ: success with no maxDistance parameter:
		location_r = requests.get(
			url=url,
			params={
				'lng': -0.9690854,
				'lat': 51.455051,
			}
		)

		self.assertEqual(location_r.status_code, 200)
		self.assertEqual(len(location_r.json()), 3)

		# READ: success with parameter maxDistance=1:
		location_r = requests.get(
			url=url,
			params={
				'lng': -0.9690854,
				'lat': 51.455051,
				'maxDistance': .001
			}
		)

		self.assertEqual(location_r.status_code, 200)
		self.assertEqual(len(location_r.json()), 2)

		# READ: success with parameter lat/lng = 0:
		location_r = requests.get(
			url=url,
			params={
				'lng': 0,
				'lat': 0,
				'maxDistance': 1
			}
		)

		self.assertEqual(location_r.status_code, 200)
		self.assertEqual(len(location_r.json()), 0)



		# Clean up: remove the test locations:
		for test_record in test_locations:
			url = self.build_url(path_parts=['api', 'locations', test_record['_id']])
			r = requests.delete(url=url)
			self.assertEqual(r.status_code, 204)




	# ************************************************************************************************************
	# START: Helper methods




	def build_test_locations(self):
		'''

		'''

		data = [
			{
				'name': 'Burger Queen',
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			},
			{
				'name': 'Starcups',
				'address': "125 High Street, Reading, RG6 1PS",
				'facilities': "Hot drinks,Food,Premium wifi",
				'lng': -0.9690884,
				'lat': 51.455061,
				'openingTimes': [
					{
						'days': "Monday - Friday",
						'opening': "7:00am",
						'closing': "5:00pm",
						'closed': False
					},
					{
						'days': "Saturday",
						'opening': "8:00am",
						'closing': "5:00pm",
						'closed': False
					},
					{
						'days': "Sunday",
						'closed': True
					},
				]
			},
			{        
				'name': 'Cafe Hero',
				'address': "555 High Street, Reading, RG6 1PS",
				'facilities': "Hot drinks,Premium wifi",
				'lng': -0.9690964,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Monday - Friday",
						'opening': "7:00am",
						'closing': "10:00pm",
						'closed': False
					},
					{
						'days': "Saturday",
						'closed': True
					},
					{
						'days': "Sunday",
						'closed': True
					},
				],
			}
		]

		# add the location data with POST requests to the api:
		url = self.build_url(path_parts=['api', 'locations'])

		response_json = list()

		for record in data:
			r = requests.post(url=url, json=record)

			if r.status_code != 201:
				print("Error writing data")
				raise ValueError("There was a problem with the POST request for {}".format(record['name']))

			response_json.append(r.json())


		return response_json



	def remove_all_records(self):
		'''


		'''

		url = self.build_url(path_parts=['api', 'locations'])

		try:
			all_loc_r = requests.get(
				url=url,
				params={
					'lng': 1,
					'lat': 1,
					'maxDistance': 100000000
				}
			)


			# test_records = all_loc_r.json()

			# print(test_records)

			# pdb.set_trace()
			
			for test_record in all_loc_r.json():
				url = self.build_url(path_parts=['api', 'locations', test_record['_id']])
				r = requests.delete(url=url)
				try:
					self.assertEqual(r.status_code, 204)

				except Exception as e:
					print("url = {}".format(url))
					print("test_record['_id'] = {}".format(test_record['_id']))
					raise e

		except Exception as e:
			pass 


	def drop_db(self):
		'''

		'''

		APITests.mongo_client.drop_database(self.db_name)



	def build_url(self, path_parts):
		'''


		'''

		# complete url
		path = '/'.join(s.strip('/') for s in path_parts)
		url = urlunsplit((self.scheme, self.url, path, None, None))


		return url 

	def location_tests(self, location_id, expected_reviews, expected_rating):
		'''

		'''

		# print("location_id = {}".format(location_id))

		# print("location_id = {}".format(location_id))
		# pdb.set_trace()

		db_location = APITests.mongo_client[self.db_name]['locations'].find_one({'_id': ObjectId(location_id)})

		self.assertEqual(db_location['rating'], expected_rating)
		
		# for whatever reason when all reviews are removed the location
		# ['reviews'] no longer exists in the database. But can add another
		# reviews without issues. When another review is added then location
		# ['reviews'] is present again.

		if db_location.get('reviews'):
			self.assertEqual(len(db_location['reviews']), expected_reviews)

		else:
			self.assertEqual(0, expected_reviews)



	def add_test_location(self, reviews):
		'''
		
		Adds a test location and up to 2 reviews each with a unique user:

		'''

		self.reset_users_collection()
		self.reset_locations_collection()

		# create a test location:
		url = self.build_url(path_parts=['api', 'locations'])
		location_r = requests.post(
			url=url,
			json={
				'name': 'Burger Queen',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 51.455051,
				'openingTimes': [
					{
						'days': "Thursday - Saturday",
						'opening': "1:00am",
						'closing': "10:00am",
						'closed': False
					},
					{
						'days': "Monday - Wednesday",
						'closed': True
					}
				]
			}
		)

		self.assertEqual(location_r.status_code, 201)
		self.assertEqual(len(location_r.json()['reviews']), 0)


		location_id = location_r.json()['_id']

		if reviews == 0:
			return (location_id)

		elif (reviews==1) or (reviews==2):

			# Review 1 / User 1
			register1_r = requests.post(
				url=self.build_url(path_parts=['api', 'register']),
				json={
					'name': "Madison Voorhees",
					'email': 'mvoorhees@hotmail.com',
					'password': 'mABC123'
				}
			)

			self.assertEqual(register1_r.status_code, 201)		
			self.assertTrue('token' in register1_r.json().keys())

			user1_token = register1_r.json()['token']


			review1_r = requests.post(
				url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
				auth=(user1_token, str(None)),
				json={
					'rating': 5,		
					'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
				}
			)

			review1_id = review1_r.json()['_id']

			self.assertEqual(review1_r.status_code, 201)
			self.assertEqual(review1_r.json()['author'], 'Madison Voorhees')
			self.assertEqual(review1_r.json()['rating'], 5)
			self.assertEqual(review1_r.json()['review_text'], 'No wifi. Has male and female a go-go dances. Will be back with the family!')

			self.location_tests(
				location_id=location_id, 
				expected_reviews=1, 
				expected_rating=5, 
			)

			if reviews == 1:
				return (location_id, review1_id, user1_token)


			# Review 2/ User 2:
			register2_r = requests.post(
				url=self.build_url(path_parts=['api', 'register']),
				json={
					'name': "Simon Hardy",
					'email': 'mhardy@hotmail.com',
					'password': 'sABC123'
				}
			)

			self.assertEqual(register2_r.status_code, 201)		
			self.assertTrue('token' in register1_r.json().keys())

			user2_token = register2_r.json()['token']


			review2_r = requests.post(
				url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
				auth=(user2_token, str(None)),
				json={	
					'rating': 2,
					'reviewText': "Didn't get any work done, great place!",
				}
			)

			review2_id = review2_r.json()['_id']
			
			self.assertEqual(review2_r.status_code, 201)
			self.assertEqual(review2_r.json()['author'], 'Simon Hardy')
			self.assertEqual(review2_r.json()['rating'], 2)
			self.assertEqual(review2_r.json()['review_text'], "Didn't get any work done, great place!")


			self.location_tests(
				location_id=location_id, 
				expected_reviews=2, 
				expected_rating=3, 
			)

			return (location_id, review1_id, user1_token, review2_id, user2_token)


		else:

			raise ValueError("reviews = {} is not valid. 0 <= reviews <= 2".format(reviews))



	def reset_users_collection(self):
		'''

		'''

		# drop users collection and recreate it with a unique index for email:
		APILocationTests.mongo_client[self.db_name].drop_collection('users')
		APILocationTests.mongo_client[self.db_name].create_collection('users')
		APILocationTests.mongo_client[self.db_name]['users'].create_index('email', unique=True)

		
	def reset_locations_collection(self):
		'''

		'''

		# drop users collection and recreate it with a unique index for email:
		APILocationTests.mongo_client[self.db_name].drop_collection('locations')
		APILocationTests.mongo_client[self.db_name].create_collection('locations')
		APILocationTests.mongo_client[self.db_name]['locations'].create_index([('coords', pymongo.GEOSPHERE)])




	def decode_token(self, token):
		'''

		'''
		load_dotenv()

		return jwt.decode(token, self._encode_key, algorithms=["HS256"])

	# End: Helper methods
	# ************************************************************************************************************


if __name__ == '__main__':
	unittest.main()









