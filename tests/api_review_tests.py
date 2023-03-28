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


