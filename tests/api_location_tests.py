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

from location_test_helpers import LocationTestHelpers

from api_endpoint_testing import APIEndPointTests, endpoint_test

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete





class APILocationTests(unittest.TestCase):

	mongo_client = None 


	@classmethod
	def setUpClass(cls):
		'''

		'''

		load_dotenv()
		
		mongo_address = os.environ.get('MONGO_URI')
		APILocationTests.mongo_client = MongoClient(mongo_address)

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

		self.helpers = LocationTestHelpers(
			mongo_client=APILocationTests.mongo_client,
			scheme='http',
			url='127.0.0.1:5000',
			db_name='myLoc8r',
		)

		# self.url = 'localhost:3000'


	# POST:/api/locations
	def test_location_create_01(self):
		'''


		'''

		self.helpers.reset_locations_collection()

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

		location_id = self.helpers.add_test_location(reviews=0)

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


		self.helpers.verify_test_location(
			location_id=location_id, 
			location_data=read1_r.json()['data'], 
			views=1
		)


	def test_location_read_02(self):
		'''
		
		14April23: Adding location.reviews.author_reviews = total number of
		reviews the author has submitted.

		'''
		
		# set up: add two locaitons with 2 reviews (2 users), and add a 2nd
		# location with 1 review by user2:

		location_id, review1_id, user1_token, review2_id, user2_token = self.helpers.add_test_location(reviews=2)

		# add a second location and a review by user2:
		location2_r = requests.post(
			url=self.helpers.build_url(path_parts=['api', 'locations']),
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

		self.assertEqual(location2_r.status_code, 201)
	
		review2_r = requests.post(
			url=self.helpers.build_url(path_parts=['api', 'locations', location2_r.json()['_id'], 'reviews']),
			auth=(user2_token, str(None)),
			json={	
				'rating': 2,
				'reviewText': "Didn't get any work done, great place!",
			}
		)
		
		self.assertEqual(review2_r.status_code, 201)

		# check each author has the correct number of reviews:

		location_r = requests.get(url=self.helpers.build_url(path_parts=['api', 'locations', location_id]))

		review1 = [x for x in location_r.json()['data']['reviews'] if x['_id'] == review1_id][0]
		review2 = [x for x in location_r.json()['data']['reviews'] if x['_id'] == review2_id][0]

		self.assertEqual(review1['author_reviews'], 1)
		self.assertEqual(review2['author_reviews'], 2)
		self.assertEqual(location_r.json()['data']['views'], 1)






	def test_location_update_01(self):
		'''


		'''

		location_id = self.helpers.add_test_location(reviews=0)
		
		# common endpoint faiulre tests. Does not do any data validation tests:
		APIEndPointTests(
			scheme=self.scheme,
			url=self.url,
			method='PUT',
			endpoint='api/locations/<parentid>',
			auth=None,
			decode_key=None,
			parent_id=location_id,
			child_id=None,
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'rating': 5,
				'lng': -0.9690854,
				'lat': 51.455051,
			},
			status_codes={"no_auth_parentid_none": 405} 
		).parent_id_endpoint_tests()


		# UPDATE unsuccessful: due to an invalid method:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'rating': 5,
				'lng': -0.9690854,
				'lat': 51.455051,
			}, 
			auth=None, 
			expected_status_code=405, 
			descriptive_error_msg="invalid method for endpoint"
		)

		self.helpers.verify_test_location(location_id=location_id)


		# UPDATE unsuccessful: due to missing invalid name field (required):
		endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data={
				'name': '',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'rating': 5,
				'lng': -0.9690854,
				'lat': 51.455051,
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="name is an empty string"
		)

		self.helpers.verify_test_location(location_id=location_id)


		# UPDATE unsuccessful: due to missing invalid address field (required):
		endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data={
				'name': 'Burger QueEn',		
				'address': "",
				'facilities': "Food,Premium wifi",
				'rating': 5,
				'lng': -0.9690854,
				'lat': 51.455051,
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="address is an empty string"
		)

		self.helpers.verify_test_location(location_id=location_id)


		# UPDATE unsuccessful: due to missing invalid rating field:
		endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'rating': 6,
				'lng': -0.9690854,
				'lat': 51.455051,
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="rating is invalid"
		)

		self.helpers.verify_test_location(location_id=location_id)


		# UPDATE unsuccessful: due to missing invalid rating field:
		endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'rating': -1,
				'lng': -0.9690854,
				'lat': 51.455051,
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="rating is invalid"
		)

		self.helpers.verify_test_location(location_id=location_id)


		# UPDATE unsuccessful: due to invalid longitude coordinate:
		endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'rating': 5,
				'lng': -180.9690854,
				'lat': 51.455051,
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="longitude is invalid"
		)

		self.helpers.verify_test_location(location_id=location_id)


		# UPDATE unsuccessful: due to invalid longitude coordinate:
		endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'rating': 5,
				'lng': 180.9690854,
				'lat': 51.455051,
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="longitude is invalid"
		)

		self.helpers.verify_test_location(location_id=location_id)


		# UPDATE unsuccessful: due to invalid latitude coordinate:
		endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'rating': 5,
				'lng': -0.9690854,
				'lat': 90.455051,
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="lattitue is invalid"
		)

		self.helpers.verify_test_location(location_id=location_id)


		# UPDATE unsuccessful: due to invalid latitude coordinate:
		endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data={
				'name': 'Burger QueEn',		
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'rating': 5,
				'lng': -0.9690854,
				'lat': -90.455051,
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="lattitue is invalid"
		)

		self.helpers.verify_test_location(location_id=location_id)


		# UPDATE successful:
		update_r = endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data={
				'name': 'Burger World',		
				'address': "1783 High Street, Reading, RG6 1PS",
				'facilities': "Food",
				'rating': 5,
				'lng': -10.9690854,
				'lat': 15.455051,
			}, 
			auth=None, 
			expected_status_code=200, 
			descriptive_error_msg="update location success"
		)

		self.assertIsInstance(ObjectId(update_r.json()['_id']), ObjectId)
		self.assertEqual(update_r.json()['name'], 'Burger World')
		self.assertEqual(update_r.json()['address'], '1783 High Street, Reading, RG6 1PS')
		self.assertEqual(update_r.json()['facilities'], 'Food')
		self.assertEqual(update_r.json()['rating'], 5)
		self.assertEqual(update_r.json()['lng'], -10.9690854)
		self.assertEqual(update_r.json()['lat'], 15.455051)
		self.assertEqual(len(update_r.json()['openingTimes']), 2)
		self.assertEqual(len(update_r.json()['reviews']), 0)



	def test_location_delete_01(self):
		'''



		'''

		location_id = self.helpers.add_test_location(reviews=0)

		# common endpoint faiulre tests. Does not do any data validation tests:
		APIEndPointTests(
			scheme=self.scheme,
			url=self.url,
			method='DELETE',
			endpoint='api/locations/<parentid>',
			auth=None,
			decode_key=None,
			parent_id=location_id,
			child_id=None,
			data=None,
			status_codes={"no_auth_parentid_none": 405} 
		).parent_id_endpoint_tests()

		self.helpers.verify_test_location(location_id=location_id)

		# DELETE failure: incorrect method:
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


		self.helpers.verify_test_location(location_id=location_id)


		# DELETE success:
		endpoint_test(
			method='DELETE', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data=None, 
			auth=None, 
			expected_status_code=204, 
			descriptive_error_msg="delete success"
		)

		endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id]), 
			data=None, 
			auth=None, 
			expected_status_code=404, 
			descriptive_error_msg="read unsuccessful because of delete success"
		)



	def test_locations_geoNear_01(self):
		'''


		'''


		# Set up: build some test locations:
		test_locations = self.helpers.build_test_locations()


		# READ: failure with no latitue parameter
		endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lng': -0.9690854,
				'maxDistance': 1
			},
			data=None, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="read unsuccessful due to no latitude parameter"
		)

		# READ: failure with invalid latitue parameter
		endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lng': -0.9690854,
				'lat': 151.455051,
				'maxDistance': 1
			},
			data=None, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="read unsuccessful due to invalid latitude parameter"
		)

		# READ: failure with invalid latitue parameter
		endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lng': -0.9690854,
				'lat': -151.455051,
				'maxDistance': 1
			},
			data=None, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="read unsuccessful due to invalid latitude parameter"
		)


		# READ: failure with missing longitude parameter
		endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lat': -51.455051,
				'maxDistance': 1
			},
			data=None, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="read unsuccessful due to invalid longitude parameter"
		)


		# READ: failure with invalid longitude parameter
		endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lng': -180.9690854,
				'lat': -51.455051,
				'maxDistance': 1
			},
			data=None, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="read unsuccessful due to invalid longitude parameter"
		)

		# READ: failure with invalid longitude parameter
		endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lng': 180.9690854,
				'lat': -51.455051,
				'maxDistance': 1
			},
			data=None, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="read unsuccessful due to invalid longitude parameter"
		)


		# READ: failure with invalid longitude parameter
		endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lng': 'abc',
				'lat': -51.455051,
				'maxDistance': 1
			},
			data=None, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="read unsuccessful due to invalid longitude parameter"
		)


		# READ: success with no maxDistance parameter:
		read1_r = endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lng': -0.9690854,
				'lat': 51.455051,
			},
			data=None, 
			auth=None, 
			expected_status_code=200, 
			descriptive_error_msg="read success with no max distance"
		)

		self.assertEqual(len(read1_r.json()['data']), 3)


		# READ: success:
		read1_r = endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lng': -0.9690854,
				'lat': 51.455051,
				'maxDistance': 0.001
			},
			data=None, 
			auth=None, 
			expected_status_code=200, 
			descriptive_error_msg="read success"
		)

		self.assertEqual(len(read1_r.json()['data']), 2)
		# self.assertEqual(len(read1_r.json()['data']), 13)



		# READ: success:
		read1_r = endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lng': 0,
				'lat': 0,
				'maxDistance': 1
			},
			data=None, 
			auth=None, 
			expected_status_code=200, 
			descriptive_error_msg="read success"
		)

		self.assertEqual(len(read1_r.json()['data']), 0)


		# READ: success with no maxDistance parameter:
		read1_r = endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations']), 
			params={
				'lng': -0.9690854,
				'lat': 51.455051,
			},
			data=None, 
			auth=None, 
			expected_status_code=200, 
			descriptive_error_msg="read success with no max distance"
		)

		self.assertEqual(len(read1_r.json()['data']), 3)






if __name__ == '__main__':
	unittest.main()









