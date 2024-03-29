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

from api_endpoint_tests import APIEndPointTests, endpoint_test

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class APITests(unittest.TestCase):

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

		APITests.mongo_client.close()



	def setUp(self):
		'''


		'''
		self.scheme = 'http'
		self.url = '127.0.0.1:5000/'
		self.db_name = 'myLoc8r'

		# self.url = 'localhost:3000'


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





	def test_location_crud_01(self):
		'''

		

		'''
		# CREATE a location:

		# unsuccessful POST due to an invalid url:
		url = self.build_url(path_parts=['api', 'locations', '6408d7ef69d46dd24edd9287'])

		location_r = requests.post(
			url=url,
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


		url = self.build_url(path_parts=['api', 'locations'])
		
		# unsuccessful POST due to missing name field (required):
		r = requests.post(
			url=url,
			json={
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

		# print(r.json())

		self.assertEqual(r.status_code, 400)


		# unsuccessful POST due to missing invalid name field (required):
		r = requests.post(
			url=url,
			json={
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
			}
		)

		# print(r.json())

		self.assertEqual(r.status_code, 400)



		# unsuccessful POST due to missing longitude coordinate (required):
		r = requests.post(
			url=url,
			json={
				'name': 'Burger Queen',
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
			}
		)

		self.assertEqual(r.status_code, 400)

		# unsuccessful POST due to invalid longitude coordinate (required):
		r = requests.post(
			url=url,
			json={
				'name': 'Burger Queen',
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
			}
		)

		# print(r.json())

		self.assertEqual(r.status_code, 400)

		# unsuccessful POST due to missing latitude coordinates (required):
		r = requests.post(
			url=url,
			json={
				'name': 'Burger Queen',
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
			}
		)

		self.assertEqual(r.status_code, 400)

		# unsuccessful POST due to invalid latitude coordinate (required):
		r = requests.post(
			url=url,
			json={
				'name': 'Burger Queen',
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690854,
				'lat': 151.455051,
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

		self.assertEqual(r.status_code, 400)

		# unsuccessful POST due to invalid openingTimes record:
		location_r = requests.post(
			url=url,
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
					
					"Monday - Wednesday",
	
				]
			}
		)

		self.assertEqual(r.status_code, 400)

		# unsuccessful POST due to missing openingTimes['days']:
		location_r = requests.post(
			url=url,
			json={
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
			}
		)

		self.assertEqual(r.status_code, 400)

		# unsuccessful POST due to invalid openingTimes['days']:
		location_r = requests.post(
			url=url,
			json={
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
			}
		)

		self.assertEqual(r.status_code, 400)

		# unsuccessful POST due to missing openingTimes['closed']:
		location_r = requests.post(
			url=url,
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
					}
				]
			}
		)

		self.assertEqual(r.status_code, 400)

		# unsuccessful POST due to invalid openingTimes['closed']:
		location_r = requests.post(
			url=url,
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
						'closed': 'True'
					}
				]
			}
		)

		self.assertEqual(r.status_code, 400)


		# a successful POST:
		location_r = requests.post(
			url=url,
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

		self.assertEqual(location_r.status_code, 201)
		self.assertEqual(location_r.json()['name'], 'Burger QueEn')


		# READ a location:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id']])
		r = requests.get(url=url)

		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json()['_id'], location_r.json()['_id'])


		# READ error due to invalid id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:]])
		r = requests.get(url=url)

		self.assertEqual(r.status_code, 404)


		# READ error due to a non existing id:
		url = self.build_url(path_parts=['api', 'locations', '6408d79c0ba5040bf57d2311'])
		r = requests.get(url=url)

		self.assertEqual(r.status_code, 404)


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




























	# def test_review_create_01(self):
	# 	'''


	# 	'''
	# 	# Set up:
	# 	self.reset_users_collection()
	# 	self.reset_locations_collection()

	# 	# create a test location:
	# 	url = self.build_url(path_parts=['api', 'locations'])
	# 	location_r = requests.post(
	# 		url=url,
	# 		json={
	# 			'name': 'Burger Queen',		
	# 			'address': "783 High Street, Reading, RG6 1PS",
	# 			'facilities': "Food,Premium wifi",
	# 			'lng': -0.9690854,
	# 			'lat': 51.455051,
	# 			'openingTimes': [
	# 				{
	# 					'days': "Thursday - Saturday",
	# 					'opening': "1:00am",
	# 					'closing': "10:00am",
	# 					'closed': False
	# 				},
	# 				{
	# 					'days': "Monday - Wednesday",
	# 					'closed': True
	# 				}
	# 			]
	# 		}
	# 	)

	# 	self.assertEqual(location_r.status_code, 201)
	# 	self.assertEqual(len(location_r.json()['reviews']), 0)


	# 	location_id = location_r.json()['_id']

	# 	# *******************************************************
	# 	# Start: create a review without any authorization:

	# 	# CREATE failure due to no credentials:
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id[1:], 'reviews']),
	# 		json={
	# 			'author': 'Simon Holmes',		
	# 			'rating': "5",
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)


	# 	# CREATE failure due to no location id:
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', 'reviews']),
	# 		json={
	# 			'author': 'Simon Holmes',		
	# 			'rating': "5",
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)


	# 	# CREATE failure due to no credentials:	
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		json={
	# 			'author': 'Simon Holmes',		
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)


	# 	# CREATE failure due to no credentials:	
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		json={
	# 			'author': 'Simon Holmes',	
	# 			'rating': 0,	
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)


	# 	# CREATE failure due to no credentials:	
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		json={
	# 			'rating': 5,		
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)


	# 	# CREATE failure due to no credentials:
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		json={
	# 			'rating': 5,
	# 			'author': '',		
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)

	# 	# CREATE failure due to no credentials:	
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		json={
	# 			'author': 'Simon Holmes',
	# 			'rating': 5,		
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)

		
	# 	# CREATE failure due to no credentials:	
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		json={
	# 			'author': 'Simon Holmes',
	# 			'rating': 5,
	# 			'reviewText': ''		
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)


	# 	# CREATE unsuccessful due to imporper request (GET not allowed):
	# 	review1_r = requests.get(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 405)

	# 	# CREATE unsuccessful due to imporper request (PUT not allowed):
	# 	review1_r = requests.put(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 405)


	# 	# CREATE unsuccessful due to imporper request (DELETE not allowed):
	# 	review1_r = requests.delete(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 405)


	# 	# Stop: create a review without any authorization:
	# 	# *******************************************************



	# 	# *******************************************************
	# 	# Start: Create a review with registration authorization:

	# 	# Add User: success:
	# 	register1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'register']),
	# 		json={
	# 			'name': "Madison Voorhees",
	# 			'email': 'mvoorhees@hotmail.com',
	# 			'password': 'mABC123'
	# 		}
	# 	)

	# 	self.assertEqual(register1_r.status_code, 201)		
	# 	self.assertTrue('token' in register1_r.json().keys())

	# 	registration_token = register1_r.json()['token']

	# 	# CREATE failure due to incorrect location id:
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id[1:], 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',		
	# 			'rating': "5",
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 404)


	# 	# CREATE failure due to no location id:
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',		
	# 			'rating': "5",
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)


	# 	# CREATE failure due to no rating (rating is a required):		
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',		
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 400)


	# 	# CREATE failure due to invalid rating:		
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',	
	# 			'rating': 0,	
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 400)


	# 	# CREATE failure due to no review text (review text is a required):		
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',
	# 			'rating': 5,		
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 400)

		
	# 	# CREATE failure due to invalid review text:		
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',
	# 			'rating': 5,
	# 			'reviewText': ''		
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 400)


	# 	# CREATE unsuccessful due to imporper request (GET not allowed):
	# 	review1_r = requests.get(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 405)

	# 	# CREATE unsuccessful due to imporper request (PUT not allowed):
	# 	review1_r = requests.put(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 405)


	# 	# CREATE unsuccessful due to imporper request (DELETE not allowed):
	# 	review1_r = requests.delete(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 405)


	# 	# CREATE failure due to invalid token:
	# 	invalid_token = self.create_invalid_token(token=registration_token)

	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(invalid_token, str(None)),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)
	# 	self.assertEqual(review1_r.json()['error'], "the authorization token is invalid")


	# 	# CREATE failure due to expired token:
	# 	expired_token = self.get_expired_token(token=registration_token)

	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(expired_token, str(None)),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)
	# 	self.assertEqual(review1_r.json()['error'], "the authorization token is expired")

	# 	# CREATE review #1 success:		
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'rating': 5,		
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)


	# 	author_data = self.decode_token(token=registration_token)

	# 	self.assertEqual(review1_r.status_code, 201)
	# 	self.assertEqual(review1_r.json()['author'], 'Madison Voorhees')
	# 	self.assertEqual(review1_r.json()['rating'], 5)
	# 	self.assertEqual(review1_r.json()['review_text'], 'No wifi. Has male and female a go-go dances. Will be back with the family!')
	# 	self.assertEqual(review1_r.json()['author_id'], author_data['_id'])

	# 	self.location_tests(
	# 		location_id=location_id, 
	# 		expected_reviews=1, 
	# 		expected_rating=5, 
	# 	)


	# 	# CREATE review #2 success:
	# 	review2_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(registration_token, str(None)),
	# 		json={
	# 			'author': 'Charlie Chaplin',		
	# 			'rating': 2,
	# 			'reviewText': "Didn't get any work done, great place!",
	# 		}
	# 	)

	# 	self.assertEqual(review2_r.status_code, 201)

	# 	# a review's author is the name of the authenticated user. If the post
	# 	# data contains an author field it is ignored.
	# 	self.assertEqual(review2_r.json()['author'], 'Madison Voorhees')
	# 	self.assertEqual(review2_r.json()['rating'], 2)
	# 	self.assertEqual(review2_r.json()['review_text'], "Didn't get any work done, great place!")
	# 	self.assertEqual(review2_r.json()['author_id'], author_data['_id'])


	# 	self.location_tests(
	# 		location_id=location_id, 
	# 		expected_reviews=2, 
	# 		expected_rating=3, 
	# 	)


	# 	# End: Create a review with authorization:	
	# 	# *******************************************************


	# 	# *******************************************************
	# 	# Start: Create a review with login authorization:

	# 	# Add User: success:
	# 	register2_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'register']),
	# 		json={
	# 			'name': "Simon Hardy",
	# 			'email': 'mhardy@hotmail.com',
	# 			'password': 'sABC123'
	# 		}
	# 	)

	# 	self.assertEqual(register2_r.status_code, 201)		
	# 	self.assertTrue('token' in register1_r.json().keys())

	# 	# login in Simon Hardy:


	# 	login1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'login']),
	# 		json={
	# 			'email': 'mhardy@hotmail.com',
	# 			'password': 'sABC123'
	# 		}
	# 	)

	# 	self.assertEqual(login1_r.status_code, 200)		
	# 	self.assertTrue('token' in login1_r.json().keys())


	# 	login_token = login1_r.json()['token']


	# 	# CREATE failure due to incorrect location id:
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id[1:], 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',		
	# 			'rating': "5",
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 404)


	# 	# CREATE failure due to no location id:
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',		
	# 			'rating': "5",
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)


	# 	# CREATE failure due to no rating (rating is a required):		
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',		
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 400)


	# 	# CREATE failure due to invalid rating:		
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',	
	# 			'rating': 0,	
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 400)



	# 	# CREATE failure due to no review text (review text is a required):		
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',
	# 			'rating': 5,		
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 400)

		
	# 	# CREATE failure due to invalid review text:		
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'author': 'Simon Holmes',
	# 			'rating': 5,
	# 			'reviewText': ''		
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 400)


	# 	# CREATE unsuccessful due to imporper request (GET not allowed):
	# 	review1_r = requests.get(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 405)

	# 	# CREATE unsuccessful due to imporper request (PUT not allowed):
	# 	review1_r = requests.put(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 405)


	# 	# CREATE unsuccessful due to imporper request (DELETE not allowed):
	# 	review1_r = requests.delete(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 405)


	# 	# CREATE failure due to invalid token:
	# 	invalid_token = self.create_invalid_token(token=login_token)

	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(invalid_token, str(None)),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)
	# 	self.assertEqual(review1_r.json()['error'], "the authorization token is invalid")



	# 	# CREATE failure due to expired token:
	# 	expired_token = self.get_expired_token(token=login_token)

	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(expired_token, str(None)),
	# 		json={
	# 			'author': 'Simmon Holmes',		
	# 			'rating': 5,
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	self.assertEqual(review1_r.status_code, 401)
	# 	self.assertEqual(review1_r.json()['error'], "the authorization token is expired")

	# 	# CREATE review #1 success:		
	# 	review1_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'rating': 5,		
	# 			'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 		}
	# 	)

	# 	author_data = self.decode_token(token=login_token)

	# 	self.assertEqual(review1_r.status_code, 201)
	# 	self.assertEqual(review1_r.json()['author'], 'Simon Hardy')
	# 	self.assertEqual(review1_r.json()['rating'], 5)
	# 	self.assertEqual(review1_r.json()['review_text'], 'No wifi. Has male and female a go-go dances. Will be back with the family!')
	# 	self.assertEqual(review1_r.json()['author_id'], author_data['_id'])


	# 	self.location_tests(
	# 		location_id=location_id, 
	# 		expected_reviews=3, 
	# 		expected_rating=4, 
	# 	)


	# 	# CREATE review #2 success:
	# 	review2_r = requests.post(
	# 		url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 		auth=(login_token, str(None)),
	# 		json={
	# 			'author': 'Charlie Chaplin',		
	# 			'rating': 2,
	# 			'reviewText': "Didn't get any work done, great place!",
	# 		}
	# 	)

	# 	self.assertEqual(review2_r.status_code, 201)

	# 	# a review's author is the name of the authenticated user. If the post
	# 	# data contains an author field it is ignored.
	# 	self.assertEqual(review2_r.json()['author'], 'Simon Hardy')
	# 	self.assertEqual(review2_r.json()['rating'], 2)
	# 	self.assertEqual(review2_r.json()['review_text'], "Didn't get any work done, great place!")
	# 	self.assertEqual(review2_r.json()['author_id'], author_data['_id'])



	# 	self.location_tests(
	# 		location_id=location_id, 
	# 		expected_reviews=4, 
	# 		expected_rating=3, 
	# 	)




	# 	# End: Create a review with login:	
	# 	# *******************************************************





	def test_review_create_01(self):
		'''


		'''
		# Set up:
		location_id = self.add_test_location(reviews=0)

		# *******************************************************
		# Start: Create a review with registration authorization:

		# Add User: success:
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

		registration_token = register1_r.json()['token']

		# common endpoint faiulre tests. Does not do any data validation tests:
		APIEndPointTests(
			scheme=self.scheme,
			url=self.url,
			method='POST',
			endpoint='api/locations/<parentid>/reviews',
			auth=(registration_token, str(None)),
			decode_key=self._encode_key,
			parent_id=location_id,
			child_id=None,
			data={
				'author': 'Simon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		).run_tests()



		# CREATE failure due to no rating (rating is a required):
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'author': 'Simon Holmes',		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}, 
			auth=(registration_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="data['rating'] is required"
		)


		# CREATE failure due to invalid rating:	
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'author': 'Simon Holmes',
				'rating': 0,		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}, 
			auth=(registration_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="data['rating'] = 0 not valid"
		)


		# CREATE failure due to no review text (review text is a required):
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'author': 'Simon Holmes',
				'rating': 0,		
			}, 
			auth=(registration_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="data['reviewText'] is required"
		)
		
		# CREATE failure due to invalid review text:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'author': 'Simon Holmes',
				'rating': 5,		
				'reviewText': "",
			}, 
			auth=(registration_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="data['reviewText'] = empty is not valid"
		)


		# CREATE review #1 success:		
		review1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'rating': 5,		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}, 
			auth=(registration_token, str(None)), 
			expected_status_code=201, 
			descriptive_error_msg="create review 1 success"
		)

		author_data = self.decode_token(token=registration_token)

		self.assertEqual(review1_r.status_code, 201)
		self.assertEqual(review1_r.json()['author'], 'Madison Voorhees')
		self.assertEqual(review1_r.json()['rating'], 5)
		self.assertEqual(review1_r.json()['review_text'], 'No wifi. Has male and female a go-go dances. Will be back with the family!')
		self.assertEqual(review1_r.json()['author_id'], author_data['_id'])

		self.location_tests(
			location_id=location_id, 
			expected_reviews=1, 
			expected_rating=5, 
		)


		# CREATE review #2 success:
		review2_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'author': 'Charlie Chaplin',		
				'rating': 2,
				'reviewText': "Didn't get any work done, great place!",
			}, 
			auth=(registration_token, str(None)), 
			expected_status_code=201, 
			descriptive_error_msg="create review 2 success"
		)


		self.assertEqual(review2_r.status_code, 201)

		# a review's author is the name of the authenticated user. If the post
		# data contains an author field it is ignored.
		self.assertEqual(review2_r.json()['author'], 'Madison Voorhees')
		self.assertEqual(review2_r.json()['rating'], 2)
		self.assertEqual(review2_r.json()['review_text'], "Didn't get any work done, great place!")
		self.assertEqual(review2_r.json()['author_id'], author_data['_id'])


		self.location_tests(
			location_id=location_id, 
			expected_reviews=2, 
			expected_rating=3, 
		)


		# End: Create a review with authorization:	
		# *******************************************************


		# *******************************************************
		# Start: Create a review with login authorization:

		# Add User: success:
		register2_r = requests.post(
			url=self.build_url(path_parts=['api', 'register']),
			json={
				'name': "Simon Hardy",
				'email': 'mhardy@hotmail.com',
				'password': 'sABC123'
			}
		)

		self.assertEqual(register2_r.status_code, 201)		
		self.assertTrue('token' in register2_r.json().keys())

		# login in Simon Hardy:
		login1_r = requests.post(
			url=self.build_url(path_parts=['api', 'login']),
			json={
				'email': 'mhardy@hotmail.com',
				'password': 'sABC123'
			}
		)

		self.assertEqual(login1_r.status_code, 200)		
		self.assertTrue('token' in login1_r.json().keys())


		login_token = login1_r.json()['token']


		# common endpoint faiulre tests. Does not do any data validation tests:
		APIEndPointTests(
			scheme=self.scheme,
			url=self.url,
			method='POST',
			endpoint='api/locations/<parentid>/reviews',
			auth=(login_token, str(None)),
			decode_key=self._encode_key,
			parent_id=location_id,
			child_id=None,
			data={
				'author': 'Simon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		).run_tests()


		# CREATE failure due to no rating (rating is a required):
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'author': 'Simon Holmes',		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}, 
			auth=(login_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="data['rating'] is required"
		)


		# CREATE failure due to invalid rating:	
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'author': 'Simon Holmes',
				'rating': 0,		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}, 
			auth=(login_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="data['rating'] = 0 not valid"
		)


		# CREATE failure due to no review text (review text is a required):
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'author': 'Simon Holmes',
				'rating': 0,		
			}, 
			auth=(login_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="data['reviewText'] is required"
		)
		
		# CREATE failure due to invalid review text:
		endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'author': 'Simon Holmes',
				'rating': 5,		
				'reviewText': "",
			}, 
			auth=(login_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="data['reviewText'] = empty is not valid"
		)


		review3_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'rating': 5,		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}, 
			auth=(login_token, str(None)), 
			expected_status_code=201, 
			descriptive_error_msg="create review 3 success"
		)

		author_data = self.decode_token(token=login_token)

		self.assertEqual(review3_r.status_code, 201)
		self.assertEqual(review3_r.json()['author'], 'Simon Hardy')
		self.assertEqual(review3_r.json()['rating'], 5)
		self.assertEqual(review3_r.json()['review_text'], 'No wifi. Has male and female a go-go dances. Will be back with the family!')
		self.assertEqual(review3_r.json()['author_id'], author_data['_id'])


		self.location_tests(
			location_id=location_id, 
			expected_reviews=3, 
			expected_rating=4, 
		)


		review4_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews']), 
			data={
				'author': 'Charlie Chaplin',		
				'rating': 2,
				'reviewText': "Didn't get any work done, great place!",
			}, 
			auth=(login_token, str(None)), 
			expected_status_code=201, 
			descriptive_error_msg="create review 4 success"
		)

		self.assertEqual(review4_r.status_code, 201)

		# a review's author is the name of the authenticated user. If the post
		# data contains an author field it is ignored.
		self.assertEqual(review4_r.json()['author'], 'Simon Hardy')
		self.assertEqual(review4_r.json()['rating'], 2)
		self.assertEqual(review4_r.json()['review_text'], "Didn't get any work done, great place!")
		self.assertEqual(review4_r.json()['author_id'], author_data['_id'])



		self.location_tests(
			location_id=location_id, 
			expected_reviews=4, 
			expected_rating=3, 
		)


		# End: Create a review with login:	
		# *******************************************************


	# 

	def test_review_read_01(self):
		'''
		
		GET review requests don't require any authorization:

		'''
		location_id, review1_id, user1_token, review2_id, user2_token = self.add_test_location(reviews=2)

		# print("location_id = {}".format(location_id))
		# print("review1_id = {}".format(review1_id))
		# print("user1_token = {}".format(user1_token))
		# print("review2_id = {}".format(review2_id))
		# print("user2_token = {}".format(user2_token))

		# common endpoint faiulre tests. Does not do any data validation tests:

		# chagning the status code for invalid PUT and DELETE request because there are
		# and endpoint for: 

		# PUT:api/locations/<parentid>/reviews/<childid> 
		# DELETE:api/locations/<parentid>/reviews/<childid> 


		# however, these endpoint requires authorization so a 401 is the
		# correct status codes.

		updated_status_codes = {
			"no_auth_put_invalid": 401,
			"no_auth_delete_invalid": 401,
		}

		APIEndPointTests(
			scheme=self.scheme,
			url=self.url,
			method='GET',
			endpoint='api/locations/<parentid>/reviews/<childid>',
			auth=None,
			decode_key=None,
			parent_id=location_id,
			child_id=review1_id,
			data=None,
			status_codes=updated_status_codes
		).run_tests()
		

		# READ success

		read_review1_r = endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review1_id]), 
			data=None, 
			auth=None, 
			expected_status_code=200, 
			descriptive_error_msg="read review 1 success"
		)

		author1_data = self.decode_token(token=user1_token)

		self.assertEqual(read_review1_r.status_code, 200)
		self.assertEqual(read_review1_r.json()['_id'], review1_id)
		self.assertEqual(read_review1_r.json()['author_id'], author1_data['_id'])


		read_review2_r = endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review2_id]), 
			data=None, 
			auth=None, 
			expected_status_code=200, 
			descriptive_error_msg="read review 1 success"
		)

		author2_data = self.decode_token(token=user2_token)

		self.assertEqual(read_review2_r.status_code, 200)
		self.assertEqual(read_review2_r.json()['_id'], review2_id)
		self.assertEqual(read_review2_r.json()['author_id'], author2_data['_id'])


		# # Testing again with authorization: Should not make a difference if
		# # autherization credentials are supplied.  However have to skip
		# # invalid method tests for PUT and DELETE because there are endpoings
		# # for these methods with authorization 
		
		# updated_status_codes = {
		# 	"auth_required_parentid_invalid": 404,
		# 	"auth_required_parentid_not_found": 404,
		# 	"auth_required_parentid_none": 404,
		# 	"auth_parentid_none": 404,

		# 	"auth_required_childid_none": 404,
		# 	"auth_required_childid_invalid": 404,
		# 	"auth_required_childid_not_found": 404,

		# 	# "no_auth_put_invalid": 401,
		# 	# "no_auth_delete_invalid": 401,

		# }

		# APIEndPointTests(
		# 	scheme=self.scheme,
		# 	url=self.url,
		# 	method='GET',
		# 	endpoint='api/locations/<parentid>/reviews/<childid>',
		# 	auth=(user1_token, str(None)),
		# 	decode_key=None,
		# 	parent_id=location_id,
		# 	child_id=review1_id,
		# 	data=None,
		# 	status_codes=updated_status_codes
		# ).run_tests()




	def test_review_update_01(self):
		'''


		'''

		location_id, review1_id, user1_token, review2_id, user2_token = self.add_test_location(reviews=2)

		print("location_id = {}".format(location_id))

		# UPDATE a review:

		# skipping .invalid_methods_tests() because there is an API endpoint for all methods
	
		APIEndPointTests(
			scheme=self.scheme,
			url=self.url,
			method='PUT',
			endpoint='api/locations/<parentid>/reviews/<childid>',
			auth=(user1_token, str(None)),
			decode_key=self._encode_key,
			parent_id=location_id,
			child_id=review1_id,
			data={
				'author': 'Simon Holmes',		
				'rating': 2,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			},
			status_codes={
				"auth_parentid_none": 404,
				"auth_required_parentid_none": 404,
				"auth_childid_none": 405,
				"auth_required_childid_none": 405,

			}
		).parent_id_endpoint_tests().child_id_endpoint_tests().authorization_tests()

		

		# UPDATE failure due to no rating (rating is required):
		update_review1_r = endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review1_id]), 
			data={
				'reviewText': "No wifi.",
			}, 
			auth=(user1_token, (None)), 
			expected_status_code=400, 
			descriptive_error_msg="update failure due to no rating"
		)


		# UPDATE failure due to no invalid rating:
		update_review1_r = endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review1_id]), 
			data={
				'rating': 6,		
				'reviewText': "No wifi.",
			}, 
			auth=(user1_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="update failure due invalid rating"
		)


		# UPDATE failure due to no reviewText (empty string):
		update_review1_r = endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review1_id]), 
			data={
				'rating': 6,		
				'reviewText': "",
			}, 
			auth=(user1_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="update failure, reviewText is empty"
		)		


		# UPDATE failure due to no reviewText:
		update_review1_r = endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review1_id]), 
			data={
				'rating': 5,		
			}, 
			auth=(user1_token, str(None)), 
			expected_status_code=400, 
			descriptive_error_msg="update failure, reviewText is missing"
		)		


		# UPDATE failure, the user credentials don't match the author of the review.
		update_review1_r = endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review1_id]), 
			data={
				'rating': 1,
				'reviewText': "No wifi."		
			}, 
			auth=(user2_token, str(None)), 
			expected_status_code=403, 
			descriptive_error_msg="update failure, user does not match author id"
		)	


		# UPDATE review 1 success:
		update_review1_r = endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review1_id]), 
			data={
				'rating': 1,
				'reviewText': "No wifi."		
			}, 
			auth=(user1_token, str(None)), 
			expected_status_code=200, 
			descriptive_error_msg="update success"
		)

		author1_data = self.decode_token(token=user1_token)

		self.assertEqual(update_review1_r.json()['_id'], review1_id)
		self.assertEqual(update_review1_r.json()['author_id'], author1_data['_id'])
		self.assertEqual(update_review1_r.json()['rating'], 1)
		self.assertEqual(update_review1_r.json()['review_text'], "No wifi.")
		self.assertEqual(update_review1_r.json()['author'], author1_data['name'])

		self.location_tests(
			location_id=location_id, 
			expected_reviews=2, 
			expected_rating=1, 
		)


		# UPDATE failure, the user credentials don't match the author of the review.
		update_review2_r = endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review2_id]), 
			data={
				'rating': 1,
				'reviewText': "No wifi."		
			}, 
			auth=(user1_token, str(None)), 
			expected_status_code=403, 
			descriptive_error_msg="update failure, user does not match author id"
		)	


		# UPDATE review 2 success:
		update_review2_r = endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review2_id]), 
			data={
				'rating': 5,
				'reviewText': "great place!"		
			}, 
			auth=(user2_token, str(None)), 
			expected_status_code=200, 
			descriptive_error_msg="update success"
		)

		author2_data = self.decode_token(token=user2_token)

		self.assertEqual(update_review2_r.json()['_id'], review2_id)
		self.assertEqual(update_review2_r.json()['author_id'], author2_data['_id'])
		self.assertEqual(update_review2_r.json()['rating'], 5)
		self.assertEqual(update_review2_r.json()['review_text'], "great place!")
		self.assertEqual(update_review2_r.json()['author'], author2_data['name'])

		self.location_tests(
			location_id=location_id, 
			expected_reviews=2, 
			expected_rating=3, 
		)	



	def test_review_delete_01(self):
		'''


		'''


		location_id, review1_id, user1_token, review2_id, user2_token = self.add_test_location(reviews=2)

		# skipping .invalid_methods_tests() because there is an API endpoint for all methods
		APIEndPointTests(
			scheme=self.scheme,
			url=self.url,
			method='DELETE',
			endpoint='api/locations/<parentid>/reviews/<childid>',
			auth=(user1_token, str(None)),
			decode_key=self._encode_key,
			parent_id=location_id,
			child_id=review1_id,
			data=None,
			status_codes={
				"auth_parentid_none": 404,
				"auth_required_parentid_none": 404,
				"auth_childid_none": 405,
				"auth_required_childid_none": 405,

			}
		).parent_id_endpoint_tests().child_id_endpoint_tests().authorization_tests()


		# DELETE failure due to invalid author:
		delete_review1_r = endpoint_test(
			method='DELETE', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review1_id]), 
			data=None, 
			auth=(user2_token, str(None)), 
			expected_status_code=403, 
			descriptive_error_msg="delete failure, user does not match author id"
		)	


		# DELETE reviw 1 success:
		delete_review1_r = endpoint_test(
			method='DELETE', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review1_id]), 
			data=None, 
			auth=(user1_token, str(None)), 
			expected_status_code=204, 
			descriptive_error_msg="delete success"
		)	



		# DELETE failure due to invalid author:
		delete_review2_r = endpoint_test(
			method='DELETE', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review2_id]), 
			data=None, 
			auth=(user1_token, str(None)), 
			expected_status_code=403, 
			descriptive_error_msg="delete failure, user does not match author id"
		)	


		# DELETE reviw 1 success:
		delete_review2_r = endpoint_test(
			method='DELETE', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'locations', location_id, 'reviews', review2_id]), 
			data=None, 
			auth=(user2_token, str(None)), 
			expected_status_code=204, 
			descriptive_error_msg="delete success"
		)





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


		


	def test_authencation_01(self):
		'''

		'''

		self.reset_users_collection()

		# Test registration:

		url = self.build_url(path_parts=['api', 'register'])

		# # Add User: failure due to no data:
		register_r = requests.post(
			url=url,
			json={}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['name'], 'name field is required')
		self.assertEqual(register_r.json()['email'], 'email field is required')
		self.assertEqual(register_r.json()['password'], 'password field is required')


		# Add User: failure due to no name in data:
		register_r = requests.post(
			url=url,
			json={
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['name'], 'name field is required')


		# Add User: failure due to empty name in data:
		register_r = requests.post(
			url=url,
			json={
				'name': "",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['name'], "a value of '' is not valid for field name")



		# Add User: failure due to empty name in data:
		register_r = requests.post(
			url=url,
			json={
				'name': "   ",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['name'], "a value of '   ' is not valid for field name")



		# Add User: failure due to no email in data:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'password': 'mABC123'
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['email'], 'email field is required')

		# Add User: failure due to empty email:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': '',
				'password': 'mABC123'
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['email'], "a value of '' is not valid for field email")


		# Add User: failure due to invalid email:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['email'], "a value of 'mcrosby15hotmail.com' is not valid for field email")



		# Add User: failure due to no password in data:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['password'], 'password field is required')


		# Add User: failure due to empty password in data:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': ''
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['password'], "a value of '' is not valid for field password")


		# Add User: failure due to password is to short:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mAB1'
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['password'], "a value of 'mAB1' is not valid for field password")


		# Add User: failure due to password requires a digit:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mAABC'
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['password'], "a value of 'mAABC' is not valid for field password")



		# Add User: failure due to password requires an upper case letter:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'macb123'
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['password'], "a value of 'macb123' is not valid for field password")


		# Add User: failure due to password requires a low case letter:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'ABC123'
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['password'], "a value of 'ABC123' is not valid for field password")



		# Add User: failure due to empty password in data:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': '   '
			}
		)

		self.assertEqual(register_r.status_code, 400)
		self.assertEqual(register_r.json()['password'], "a value of '   ' is not valid for field password")


		# Add User: success:
		register_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(register_r.status_code, 201)		
		self.assertTrue('token' in register_r.json().keys())

		# time.sleep(1)

		# Add User: failure because the user already exists:
		register_r = requests.post(
			url=url,
			json={
				'name': "Simon Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(register_r.status_code, 400)		
		self.assertEqual(register_r.json()['error'], "A user for mcrosby15@hotmail.com already exists")

		# Test login:

		url = self.build_url(path_parts=['api', 'login'])

		# Login User: failure due to no data:
		login_r = requests.post(
			url=url,
			json={}
		)

		self.assertEqual(login_r.status_code, 400)
		# self.assertEqual(login_r.json()['name'], 'name field is required')
		self.assertEqual(login_r.json()['email'], 'email field is required')
		self.assertEqual(login_r.json()['password'], 'password field is required')


		# # Login User: failure due to no name in data:
		# login_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'email': 'mcrosby15@hotmail.com',
		# 		'password': 'mABC123'
		# 	}
		# )

		# self.assertEqual(login_r.status_code, 400)
		# self.assertEqual(login_r.json()['name'], 'name field is required')


		# # Login User: failure due to empty name in data:
		# login_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': "",
		# 		'email': 'mcrosby15@hotmail.com',
		# 		'password': 'mABC123'
		# 	}
		# )

		# self.assertEqual(login_r.status_code, 400)
		# self.assertEqual(login_r.json()['name'], "a value of '' is not valid for field name")



		# # Login User: failure due to empty name in data:
		# login_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': "   ",
		# 		'email': 'mcrosby15@hotmail.com',
		# 		'password': 'mABC123'
		# 	}
		# )

		# self.assertEqual(login_r.status_code, 400)
		# self.assertEqual(login_r.json()['name'], "a value of '   ' is not valid for field name")



		# Login User: failure due to no email in data:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'password': 'mABC123'
			}
		)

		self.assertEqual(login_r.status_code, 400)
		self.assertEqual(login_r.json()['email'], 'email field is required')


		# Login User: failure due to empty email:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': '',
				'password': 'mABC123'
			}
		)

		self.assertEqual(login_r.status_code, 400)
		self.assertEqual(login_r.json()['email'], "a value of '' is not valid for field email")


		# Login User: failure due to invalid email:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(login_r.status_code, 400)
		self.assertEqual(login_r.json()['email'], "a value of 'mcrosby15hotmail.com' is not valid for field email")


		# Login User: failure due to no password in data:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
			}
		)

		self.assertEqual(login_r.status_code, 400)
		self.assertEqual(login_r.json()['password'], 'password field is required')


		# Login User: failure due to empty password in data:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': ''
			}
		)

		self.assertEqual(login_r.status_code, 400)
		self.assertEqual(login_r.json()['password'], "a value of '' is not valid for field password")


		# Login User: failure due to password is to short:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mAB1'
			}
		)

		self.assertEqual(login_r.status_code, 400)
		self.assertEqual(login_r.json()['password'], "a value of 'mAB1' is not valid for field password")


		# Login User: failure due to password requires a digit:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mAABC'
			}
		)

		self.assertEqual(login_r.status_code, 400)
		self.assertEqual(login_r.json()['password'], "a value of 'mAABC' is not valid for field password")



		# Login User: failure due to password requires an upper case letter:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'macb123'
			}
		)

		self.assertEqual(login_r.status_code, 400)
		self.assertEqual(login_r.json()['password'], "a value of 'macb123' is not valid for field password")


		# Login User: failure due to password requires a low case letter:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'ABC123'
			}
		)

		self.assertEqual(login_r.status_code, 400)
		self.assertEqual(login_r.json()['password'], "a value of 'ABC123' is not valid for field password")



		# Login User: failure due to empty password in data:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': '   '
			}
		)

		self.assertEqual(login_r.status_code, 400)
		self.assertEqual(login_r.json()['password'], "a value of '   ' is not valid for field password")


		# Login User: failure due to incorrect password:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC1234'
			}
		)

		self.assertEqual(login_r.status_code, 401)
		self.assertEqual(login_r.json()['error'], "password for mcrosby15@hotmail.com is incorrect.")


		# Login User: success:
		login_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(login_r.status_code, 200)		
		self.assertTrue('token' in login_r.json().keys())


		# Login User: failure because the user does exists:
		login_r = requests.post(
			url=url,
			json={
				'name': "Simon Crosby",
				'email': 'scrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(login_r.status_code, 400)		
		self.assertEqual(login_r.json()['error'], "No user for email scrosby15@hotmail.com")

	# ************************************************************************************************************
	# START: Helper methods



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
		APITests.mongo_client[self.db_name].drop_collection('users')
		APITests.mongo_client[self.db_name].create_collection('users')
		APITests.mongo_client[self.db_name]['users'].create_index('email', unique=True)

		
	def reset_locations_collection(self):
		'''

		'''

		# drop users collection and recreate it with a unique index for email:
		APITests.mongo_client[self.db_name].drop_collection('locations')
		APITests.mongo_client[self.db_name].create_collection('locations')
		APITests.mongo_client[self.db_name]['locations'].create_index([('coords', pymongo.GEOSPHERE)])




	def decode_token(self, token):
		'''

		'''
		load_dotenv()

		return jwt.decode(token, self._encode_key, algorithms=["HS256"])

	# End: Helper methods
	# ************************************************************************************************************




if __name__ == '__main__':
	unittest.main()





	# def test_review_crud_01(self):
		
	# 	'''
		


	# 	'''

	# 	pass 
		
		# # create a test location and then add reviews:
		# url = self.build_url(path_parts=['api', 'locations'])
		# location_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'name': 'Burger Queen',		
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
		# self.assertEqual(len(location_r.json()['reviews']), 0)

		# # CREATE a review:

		# # CREATE failure due to incorrect location id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews'])
		# review1_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'rating': "5",
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 404)


		# # CREATE failure due to no location id:
		# url = self.build_url(path_parts=['api', 'locations', 'reviews'])
		# review1_r = requests.post(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'rating': "5",
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 401)


		# # CREATE failure due to no rating (rating is a required):		
		# review1_r = requests.post(
		# 	url=self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews']),
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 400)


		# # CREATE failure due to invalid rating:		
		# review1_r = requests.post(
		# 	url=self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews']),
		# 	json={
		# 		'author': 'Simon Holmes',	
		# 		'rating': 0,	
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 400)



		# # CREATE failure due to no author (author is a required):		
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_r = requests.post(
		# 	url=self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews']),
		# 	json={
		# 		'rating': 5,		
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 400)


		# # CREATE failure due to invalid author:		
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_r = requests.post(
		# 	url=self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews']),
		# 	json={
		# 		'rating': 5,
		# 		'author': '',		
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 400)

		# # CREATE failure due to no review text (review text is a required):		
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_r = requests.post(
		# 	url=self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews']),
		# 	json={
		# 		'author': 'Simon Holmes',
		# 		'rating': 5,		
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 400)

		
		# # CREATE failure due to invalid review text:		
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_r = requests.post(
		# 	url=self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews']),
		# 	json={
		# 		'author': 'Simon Holmes',
		# 		'rating': 5,
		# 		'reviewText': ''		
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 400)




		# # CREATE unsuccessful due to imporper request (GET not allowed):
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_r = requests.get(
		# 	url=url,
		# 	json={
		# 		'author': 'Simmon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 405)

		# # CREATE unsuccessful due to imporper request (PUT not allowed):
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Simmon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 405)


		# # CREATE unsuccessful due to imporper request (DELETE not allowed):
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_r = requests.delete(
		# 	url=url,
		# 	json={
		# 		'author': 'Simmon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 405)

		
		# # CREATE review #1 success:
		# location_id = location_r.json()['_id']

		# # url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_r = requests.post(
		# 	url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
		# 	json={
		# 		'author': 'Simmon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 201)


		# # self.assertTrue('_id' in review1_r.json())

		# # self.assertTrue('_id' in review1_r.json())

		# # read location and verify the review was added and rating updated:

		# # location_r = self.location_tests(
		# # 	location_id='640c131b0eff6bceca9e57b8', 
		# # 	expected_reviews=1, 
		# # 	expected_rating=5, 
		# # )


		# self.location_tests(
		# 	location_id=location_id, 
		# 	expected_reviews=1, 
		# 	expected_rating=5, 
		# )
		


		# # CREATE review #2 success:

		# # url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review2_r = requests.post(
		# 	url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
		# 	json={
		# 		'author': 'Charlie Chaplin',		
		# 		'rating': 2,
		# 		'reviewText': "Didn't get any work done, great place!",
		# 	}
		# )

		# self.assertEqual(review2_r.status_code, 201)

		# # read location and verify the review was added and rating updated:

		# self.location_tests(
		# 	location_id=location_id, 
		# 	expected_reviews=2, 
		# 	expected_rating=3, 
		# )



		# # READ a review:

		# # READ failure due to incorrect location id:
		# # url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review1_r.json()['_id']])

		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review1_r.json()['_id']])
		# review1_err_r = requests.get(url=url)
		# self.assertEqual(review1_err_r.status_code, 404)

		# # READ failure due to no location id:
		# url = self.build_url(path_parts=['api', 'locations', 'reviews', review1_r.json()['_id']])
		# review1_err_r = requests.get(url=url)
		# self.assertEqual(review1_err_r.status_code, 404)


		# # READ failure due to non existing location id:
		# url = self.build_url(path_parts=['api', 'locations', '640ceee95fedd040ba74a736', 'reviews', review1_r.json()['_id'][1:]])
		# review1_err_r = requests.get(url=url)
		# self.assertEqual(review1_err_r.status_code, 404)


		# # READ failure due to incorrect review id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id'][1:]])
		# review1_err_r = requests.get(url=url)
		# self.assertEqual(review1_err_r.status_code, 404)


		# # READ failure due non exixting review id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', '640ceee95fedd040ba74a736'])
		# review1_err_r = requests.get(url=url)
		# self.assertEqual(review1_err_r.status_code, 404)


		# # READ failure due to no review id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_err_r = requests.get(url=url)
		# self.assertEqual(review1_err_r.status_code, 405)
		

		# # READ success
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id']])
		# read_review1_r = requests.get(url=url)
		# self.assertEqual(read_review1_r.status_code, 200)
		# self.assertEqual(read_review1_r.json()['_id'], review1_r.json()['_id'])


		# # UPDATE a review:


		# # UPDATE failure due to incorrect location id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review1_r.json()['_id']])
		# review1_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )
		# self.assertEqual(review1_update_r.status_code, 404)


		# # UPDATE failure due to non existing location id:
		# url = self.build_url(path_parts=['api', 'locations', '640ceee95fedd040ba74a736', 'reviews', review1_r.json()['_id']])
		# review1_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )
		# self.assertEqual(review1_update_r.status_code, 404)


		# # UPDATE failure due to no location id:
		# url = self.build_url(path_parts=['api', 'locations', 'reviews', review1_r.json()['_id']])
		# review1_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )
		# self.assertEqual(review1_update_r.status_code, 404)

		# # UPDATE failure due to incorrect review id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id'][1:]])
		# review1_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )
		# self.assertEqual(review1_update_r.status_code, 404)


		# # UPDATE failure due to non existing review id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', '640ceee95fedd040ba74a736'])
		# review1_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )
		# self.assertEqual(review1_update_r.status_code, 404)

		# # UPDATE failure due to no review id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )
		# self.assertEqual(review1_update_r.status_code, 405)
		

		# # UPDATE failure due to no rating (rating is required):
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id']])
		# review1_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )
		# self.assertEqual(review1_update_r.status_code, 400)


		# # UPDATE failure due to no author (author is required):
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id']])
		# review1_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )
		# self.assertEqual(review1_update_r.status_code, 400)


		# # UPDATE failure due to no review text (review is required):
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id']])
		# review1_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'author': 5,
		# 	}
		# )
		# self.assertEqual(review1_update_r.status_code, 400)


		# # UPDATE success

		# # author needs to be correct from 'Simmon Holmes' to 'Simon Holmes'
		# self.assertEqual(review1_r.json()['author'], 'Simmon Holmes')

		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id']])
		# review1_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Simon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )
		# self.assertEqual(review1_update_r.status_code, 200)

		# self.location_tests(
		# 	location_id=location_r.json()['_id'], 
		# 	expected_reviews=2, 
		# 	expected_rating=3, 
		# )

		# # updated_review = location_r.json()['reviews'][0]
		# self.assertEqual(review1_update_r.json()['author'], 'Simon Holmes')

		# # update the second review's rating to 5
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review2_r.json()['_id']])

		# review2_update_r = requests.put(
		# 	url=url,
		# 	json={
		# 		'author': 'Charlie Chaplin',		
		# 		'rating': 5,
		# 		'reviewText': "Didn't get any work done, great place!",
		# 	}
		# )

		# self.assertEqual(review2_update_r.status_code, 200)

		# self.location_tests(
		# 	location_id=location_r.json()['_id'], 
		# 	expected_reviews=2, 
		# 	expected_rating=5, 
		# )

		# # DELETE a review:

		# # DELETE failure due to incorrect location id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review2_r.json()['_id']])
		# review2_delete_r = requests.delete(url=url)
		# self.assertEqual(review2_delete_r.status_code, 404)

		# # DELETE failure due to non existing location id:
		# url = self.build_url(path_parts=['api', 'locations', '640ceee95fedd040ba74a736', 'reviews', review2_r.json()['_id']])
		# review2_delete_r = requests.delete(url=url)
		# self.assertEqual(review2_delete_r.status_code, 404)

		# # DELETE failure due to no location id:
		# url = self.build_url(path_parts=['api', 'locations', 'reviews', review2_r.json()['_id']])
		# review2_delete_r = requests.delete(url=url)
		# self.assertEqual(review2_delete_r.status_code, 404)
		
		# # DELETE failure due to incorrect review id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review2_r.json()['_id'][1:]])
		# review2_delete_r = requests.delete(url=url)
		# self.assertEqual(review2_delete_r.status_code, 404)


		# # DELETE failure due to non existing review id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', '640ceee95fedd040ba74a736'])
		# review2_delete_r = requests.delete(url=url)
		# self.assertEqual(review2_delete_r.status_code, 404)
		
		# # DELETE failure due to no review id. Without a review id the api
		# # endpoint becomes /api/locations/<locationid>/reviews and delete is
		# # an invalid method for this endpoint.
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review2_delete_r = requests.delete(url=url)
		# self.assertEqual(review2_delete_r.status_code, 405)
		
		# # DELETE 2nd review: success
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review2_r.json()['_id']])
		# read_review_1 = requests.get(url)
		# self.assertEqual(read_review_1.status_code, 200)

		# review2_delete_r = requests.delete(url=url)
		# self.assertEqual(review2_delete_r.status_code, 204)

		# read_review_1 = requests.get(url)
		# self.assertEqual(read_review_1.status_code, 404)

		# self.location_tests(
		# 	location_id=location_r.json()['_id'], 
		# 	expected_reviews=1, 
		# 	expected_rating=5, 
		# )

		# # DELETE 1st review: success
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id']])
		# read_review_2 = requests.get(url)
		# self.assertEqual(read_review_2.status_code, 200)

		# review2_delete_r = requests.delete(url=url)
		# self.assertEqual(review2_delete_r.status_code, 204)

		# self.location_tests(
		# 	location_id=location_r.json()['_id'], 
		# 	expected_reviews=0, 
		# 	expected_rating=0, 
		# )

		# read_review_2 = requests.get(url)
		# self.assertEqual(read_review_2.status_code, 404)


		# # for whatever reason when all reviews are removed location
		# # ['reviews'] no longer exists for the location. But can add another
		# # reviews without issues. When another review is added then location
		# # ['reviews'] is present again.

		# # CREATE review #1 success:
		# location_id = location_r.json()['_id']

		# # url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		# review1_r = requests.post(
		# 	url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
		# 	json={
		# 		'author': 'Simmon Holmes',		
		# 		'rating': 5,
		# 		'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
		# 	}
		# )

		# self.assertEqual(review1_r.status_code, 201)


		# # Clean up; delete the test location:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id']])
		# r = requests.delete(url=url)
		# self.assertEqual(r.status_code, 204)
















