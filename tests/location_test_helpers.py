import unittest
from bson import ObjectId
from urllib.parse import urlsplit, urlunsplit

# from pymongo import MongoClient
import pymongo

# import collections

# import datetime
# import time 

# import tzlocal
# import pytz

import requests

import jwt
from dotenv import load_dotenv
import os


import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class LocationTestHelpers(object):
	'''

	Common helper methods for location API tests.

	'''

	def __init__(self, mongo_client, scheme, url, db_name, encode_key=None):
		
		self._mongo_client = mongo_client
		self._scheme = scheme
		self._url = url 
		self._db_name = db_name
		self._encode_key = encode_key



	# ************************************************************************************************************
	# START: Helper methods


	def verify_test_location(self, location_id, location_data=None, views=None):


		if location_data is None:
			read_r = requests.get(
				url=self.build_url(path_parts=['api', 'locations', location_id])
			)

			unittest.TestCase().assertEqual(read_r.status_code, 200)

			location_data = read_r.json()['data']


		unittest.TestCase().assertEqual(location_data['_id'], location_id)
		unittest.TestCase().assertEqual(location_data['name'], 'Burger Queen')
		unittest.TestCase().assertEqual(location_data['address'], '783 High Street, Reading, RG6 1PS')
		unittest.TestCase().assertEqual(location_data['facilities'], 'Food,Premium wifi')
		unittest.TestCase().assertEqual(location_data['rating'], 0)
		unittest.TestCase().assertEqual(location_data['lng'], -0.9690854)
		unittest.TestCase().assertEqual(location_data['lat'], 51.455051)
		unittest.TestCase().assertEqual(len(location_data['openingTimes']), 2)
		unittest.TestCase().assertEqual(len(location_data['reviews']), 0)

		if views:
			unittest.TestCase().assertEqual(location_data['views'], views)


		# read_r = requests.get(
		# 	url=self.build_url(path_parts=['api', 'locations', location_id])
		# )

		# unittest.TestCase().assertEqual(read_r.status_code, 200)

		# unittest.TestCase().assertEqual(read_r.json()['_id'], location_id)
		# unittest.TestCase().assertEqual(read_r.json()['name'], 'Burger Queen')
		# unittest.TestCase().assertEqual(read_r.json()['address'], '783 High Street, Reading, RG6 1PS')
		# unittest.TestCase().assertEqual(read_r.json()['facilities'], 'Food,Premium wifi')
		# unittest.TestCase().assertEqual(read_r.json()['rating'], 0)
		# unittest.TestCase().assertEqual(read_r.json()['lng'], -0.9690854)
		# unittest.TestCase().assertEqual(read_r.json()['lat'], 51.455051)
		# unittest.TestCase().assertEqual(len(read_r.json()['openingTimes']), 2)
		# unittest.TestCase().assertEqual(len(read_r.json()['reviews']), 0)




	def build_test_locations(self):
		'''

		'''
	
		self.reset_locations_collection()
		
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
					unittest.TestCase().assertEqual(r.status_code, 204)

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
		url = urlunsplit((self._scheme, self._url, path, None, None))


		return url 

	def location_tests(self, location_id, expected_reviews, expected_rating):
		'''

		'''

		# print("location_id = {}".format(location_id))

		# print("location_id = {}".format(location_id))
		# pdb.set_trace()

		db_location = self._mongo_client[self._db_name]['locations'].find_one({'_id': ObjectId(location_id)})

		unittest.TestCase().assertEqual(db_location['rating'], expected_rating)
		
		# for whatever reason when all reviews are removed the location
		# ['reviews'] no longer exists in the database. But can add another
		# reviews without issues. When another review is added then location
		# ['reviews'] is present again.

		if db_location.get('reviews'):
			unittest.TestCase().assertEqual(len(db_location['reviews']), expected_reviews)

		else:
			unittest.TestCase().assertEqual(0, expected_reviews)



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

		unittest.TestCase().assertEqual(location_r.status_code, 201)
		unittest.TestCase().assertEqual(len(location_r.json()['reviews']), 0)


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

			unittest.TestCase().assertEqual(register1_r.status_code, 201)		
			unittest.TestCase().assertTrue('token' in register1_r.json().keys())

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

			unittest.TestCase().assertEqual(review1_r.status_code, 201)
			unittest.TestCase().assertEqual(review1_r.json()['author'], 'Madison Voorhees')
			unittest.TestCase().assertEqual(review1_r.json()['rating'], 5)
			unittest.TestCase().assertEqual(review1_r.json()['review_text'], 'No wifi. Has male and female a go-go dances. Will be back with the family!')

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

			unittest.TestCase().assertEqual(register2_r.status_code, 201)		
			unittest.TestCase().assertTrue('token' in register1_r.json().keys())

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
			
			unittest.TestCase().assertEqual(review2_r.status_code, 201)
			unittest.TestCase().assertEqual(review2_r.json()['author'], 'Simon Hardy')
			unittest.TestCase().assertEqual(review2_r.json()['rating'], 2)
			unittest.TestCase().assertEqual(review2_r.json()['review_text'], "Didn't get any work done, great place!")


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
		self._mongo_client[self._db_name].drop_collection('users')
		self._mongo_client[self._db_name].create_collection('users')
		self._mongo_client[self._db_name]['users'].create_index('email', unique=True)

		
	def reset_locations_collection(self):
		'''

		'''

		# drop users collection and recreate it with a unique index for email:
		self._mongo_client[self._db_name].drop_collection('locations')
		self._mongo_client[self._db_name].create_collection('locations')
		self._mongo_client[self._db_name]['locations'].create_index([('coords', pymongo.GEOSPHERE)])




	def decode_token(self, token):
		'''

		'''
		load_dotenv()

		return jwt.decode(token, self._encode_key, algorithms=["HS256"])




	def test_profile_pic_added(self, token):
		'''

		'''

		token_data = self.decode_token(token=token)


		profile_path = os.path.join('/Users/glenn/Documents/GettingMEAN/my_loc8r/src/my_loc8r_app', 'profiles')


		filenames = [x.split('.')[0] for x in os.listdir(profile_path)]

		unittest.TestCase().assertIn(token_data['_id'], filenames)


	def test_remove_pic(self, token):

		token_data = self.decode_token(token=token)

		profile_path = os.path.join('/Users/glenn/Documents/GettingMEAN/my_loc8r/src/my_loc8r_app', 'profiles')

		# very unsophisticated delete:

		filenames = ["{}.png".format(token_data['_id']), "{}.jpg".format(token_data['_id']), "{}.jpeg".format(token_data['_id'])]

		for filename in filenames:
			this_path = os.path.join(profile_path, filename)

			if os.path.exists(this_path):
				os.remove(this_path)
		

		# try:

		# 	filename = "{}.png".format(token_data['_id'])
		# 	os.remove(os.path.join(profiles_path, filename))

		# 	# os.remove("/Users/glenn/Documents/GettingMEAN/my_loc8r/profiles/{}.png".format(token_data['_id']))

		# except Exception as e:
		# 	pass 


		# try:

		# 	filename = "{}.jpg".format(token_data['_id'])
		# 	os.remove(os.path.join(profiles_path, filename))


		# 	# os.remove("/Users/glenn/Documents/GettingMEAN/my_loc8r/profiles/{}.jpg".format(token_data['_id']))

		# except Exception as e:
		# 	pass 


		# try:
		# 	filename = "{}.jpeg".format(token_data['_id'])
		# 	os.remove(os.path.join(profiles_path, filename))

		# 	# os.remove("/Users/glenn/Documents/GettingMEAN/my_loc8r/profiles/{}.jpeg".format(token_data['_id']))

		# except Exception as e:
		# 	pass 







	# End: Helper methods
	# ************************************************************************************************************





































