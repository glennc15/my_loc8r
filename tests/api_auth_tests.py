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

# from api_endpoint_testing import APIEndPointTests, endpoint_test

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


	def build_url(self, path_parts):
		'''


		'''

		# complete url
		path = '/'.join(s.strip('/') for s in path_parts)
		url = urlunsplit((self.scheme, self.url, path, None, None))


		return url 



	def reset_users_collection(self):
		'''

		'''

		# drop users collection and recreate it with a unique index for email:
		APITests.mongo_client[self.db_name].drop_collection('users')
		APITests.mongo_client[self.db_name].create_collection('users')
		APITests.mongo_client[self.db_name]['users'].create_index('email', unique=True)


	# End: Helper methods
	# ************************************************************************************************************




if __name__ == '__main__':
	unittest.main()

