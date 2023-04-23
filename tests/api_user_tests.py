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

from location_test_helpers import LocationTestHelpers
from api_endpoint_testing import APIEndPointTests, endpoint_test

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class APIUserTests(unittest.TestCase):

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

		APIUserTests.mongo_client.close()



	def setUp(self):
		'''


		'''
		self.scheme = 'http'
		self.url = '127.0.0.1:5000'
		self.db_name = 'myLoc8r'

		self.helpers = LocationTestHelpers(
			mongo_client=APIUserTests.mongo_client,
			scheme='http',
			url='127.0.0.1:5000',
			db_name='myLoc8r',
			encode_key=APIUserTests._encode_key
		)


	def test_registration_01(self):
		'''


		'''


		self.helpers.reset_users_collection()

		# Test registration:

		url = self.helpers.build_url(path_parts=['api', 'register'])





		# Add User: failure due to no data:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: no data"
		)

		self.assertEqual(register1_r.json()['name'], 'name field is required')
		self.assertEqual(register1_r.json()['email'], 'email field is required')
		self.assertEqual(register1_r.json()['password'], 'password field is required')


		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: no name"
		)

		self.assertEqual(register1_r.json()['name'], 'name field is required')


		# Add User: failure due to empty name in data:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: empty name 1"
		)


		self.assertEqual(register1_r.json()['name'], "a value of '' is not valid for field name")



		# Add User: failure due to empty name in data:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "   ",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: empty name 2"
		)

		self.assertEqual(register1_r.json()['name'], "a value of '   ' is not valid for field name")



		# Add User: failure due to no email in data:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: no email"
		)

		self.assertEqual(register1_r.json()['email'], 'email field is required')


		# Add User: failure due to empty email:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': '   ',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: empty email 1"
		)


		self.assertEqual(register1_r.json()['email'], "a value of '   ' is not valid for field email")


		# Add User: failure due to invalid email:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: invalid email"
		)


		self.assertEqual(register1_r.json()['email'], "a value of 'mvoorhees15hotmail.com' is not valid for field email")



		# Add User: failure due to no password in data:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: no password"
		)

		self.assertEqual(register1_r.json()['password'], 'password field is required')


		# Add User: failure due to empty password in data:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': ''			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: empty password"
		)

		self.assertEqual(register1_r.json()['password'], "a value of '' is not valid for field password")


		# Add User: failure due to password is to short:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mAB1'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: password invalid 1"
		)
 
		self.assertEqual(register1_r.json()['password'], "a value of 'mAB1' is not valid for field password")


		# Add User: failure due to password requires a digit:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mAABC'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: password invalid 2"
		)
 
		self.assertEqual(register1_r.json()['password'], "a value of 'mAABC' is not valid for field password")



		# Add User: failure due to password requires an upper case letter:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'macb123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: invalid password 3"
		)
 
		self.assertEqual(register1_r.json()['password'], "a value of 'macb123' is not valid for field password")


		# Add User: failure due to password requires a low case letter:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'ABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: invalid password 4"
		)
 
		self.assertEqual(register1_r.json()['password'], "a value of 'ABC123' is not valid for field password")



		# Add User: failure due to empty password in data:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': '   '			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: invalid password 5"
		)

		self.assertEqual(register1_r.json()['password'], "a value of '   ' is not valid for field password")


		# Add User: success:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=201, 
			descriptive_error_msg="registration success"
		)
		

		self.assertTrue('token' in register1_r.json().keys())


		# Add User: failure because the user already exists:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="registration failure: user already exists"
		)
	
		self.assertEqual(register1_r.json()['error'], "A user for mvoorhees15@hotmail.com already exists")


	def test_login_01(self):
		'''


		'''

		# Set up:

		self.helpers.reset_users_collection()

		# Add User: success:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=201, 
			descriptive_error_msg="registration success"
		)
		

		self.assertTrue('token' in register1_r.json().keys())


		# Test logins:


		# Login User: failure due to no data:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: no data"
		)

		self.assertEqual(login1_r.json()['email'], 'email field is required')
		self.assertEqual(login1_r.json()['password'], 'password field is required')


		# Login User: failure due to no email in data:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: no email"
		)
 
		self.assertEqual(login1_r.json()['email'], 'email field is required')


		# Login User: failure due to empty email:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': '',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: invalid email 1"
		)

		self.assertEqual(login1_r.json()['email'], "a value of '' is not valid for field email")


		# Login User: failure due to invalid email:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: invalid email 2"
		)

		self.assertEqual(login1_r.json()['email'], "a value of 'mvoorhees15hotmail.com' is not valid for field email")


		# Login User: failure due to no password in data:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: no password"
		)

		self.assertEqual(login1_r.json()['password'], 'password field is required')


		# Login User: failure due to empty password in data:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
				'password': ''			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: invalid password 1"
		)

		self.assertEqual(login1_r.json()['password'], "a value of '' is not valid for field password")


		# Login User: failure due to password is to short:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mAB1'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: invalid password 2"
		)

		self.assertEqual(login1_r.json()['password'], "a value of 'mAB1' is not valid for field password")


		# Login User: failure due to password requires a digit:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mAABC'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: invalid password 3"
		)
 
		self.assertEqual(login1_r.json()['password'], "a value of 'mAABC' is not valid for field password")



		# Login User: failure due to password requires an upper case letter:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
				'password': 'macb123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: invalid password 4"
		)

		self.assertEqual(login1_r.json()['password'], "a value of 'macb123' is not valid for field password")


		# Login User: failure due to password requires a low case letter:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
				'password': 'ABC123'			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: invalid password 5"
		)

		self.assertEqual(login1_r.json()['password'], "a value of 'ABC123' is not valid for field password")



		# Login User: failure due to empty password in data:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
				'password': '   '			
			}, 
			auth=None, 
			expected_status_code=400, 
			descriptive_error_msg="login failure: invalid password 6"
		)

		self.assertEqual(login1_r.json()['password'], "a value of '   ' is not valid for field password")


		# Login User: failure due to incorrect password:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC1234'			
			}, 
			auth=None, 
			expected_status_code=401, 
			descriptive_error_msg="login failure: incorrect password"
		)

		self.assertEqual(login1_r.json()['error'], "password for mvoorhees15@hotmail.com is incorrect.")


		# Login User: success 1:
		login1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=200, 
			descriptive_error_msg="login success 1"
		)

		self.assertTrue('token' in login1_r.json().keys())


		# Login User: success 2:
		login2_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'login']), 
			data={
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=200, 
			descriptive_error_msg="login success 2"
		)

		self.assertEqual(login1_r.status_code, 200)		
		self.assertTrue('token' in login2_r.json().keys())


	def test_profile_01(self):

		self.helpers.reset_users_collection()


		# Add User: success:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=201, 
			descriptive_error_msg="registration success"
		)
		
		self.assertTrue('token' in register1_r.json().keys())


		token = register1_r.json()['token']

		# profile pic data:
		file1 = open('/Users/glenn/Documents/GettingMEAN/my_loc8r/tests/profile_pic/bug1.png', 'rb')
		profile1 = {'file': file1}


		# invalid methods:

		# Add Profile pic: failure due to invalid method:
		profile1_r = endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'userprofile']), 
			data=None,
			auth=(token, str(None)), 
			expected_status_code=404, 
			descriptive_error_msg="invalid method: GET"
		)

		# Add Profile pic: failure due to invalid method:
		profile1_r = endpoint_test(
			method='PUT', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'userprofile']), 
			data=None,
			auth=(token, str(None)), 
			expected_status_code=405, 
			descriptive_error_msg="invalid method: PUT"
		)

		# Add Profile pic: failure due to invalid method:
		profile1_r = endpoint_test(
			method='DELETE', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'userprofile']), 
			data=None,
			auth=(token, str(None)), 
			expected_status_code=405, 
			descriptive_error_msg="invalid method: DELETE"
		)


		# Add Profile pic: failure due to no authorization:
		profile1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'userprofile']), 
			data=None,
			auth=None, 
			files=profile1,
			expected_status_code=401, 
			descriptive_error_msg="failuer: no authorization"
		)


		# Add Profile pic: failure due to no file1:
		profile1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'userprofile']), 
			data=None,
			auth=(token, str(None)), 
			files={},
			expected_status_code=400, 
			descriptive_error_msg="failuer: no file1"
		)


		# Add Profile pic: failure due to no file2:
		profile1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'userprofile']), 
			data=None,
			auth=(token, str(None)), 
			files={'file': ''},
			expected_status_code=400, 
			descriptive_error_msg="failuer: no file2"
		)


		# Add Profile pic: failure due invalid file type:
		file2 = open('/Users/glenn/Documents/GettingMEAN/my_loc8r/tests/profile_pic/little-ant-having-arms-up.zip', 'rb')
		profile1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'userprofile']), 
			data=None,
			auth=(token, str(None)), 
			files={'file': file2},
			expected_status_code=400, 
			descriptive_error_msg="failuer: invalid file type"
		)



		# Add Profile pic: success:
		profile1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'userprofile']), 
			data=None,
			auth=(token, str(None)), 
			files=profile1,
			expected_status_code=200, 
			descriptive_error_msg="success, add first profile pic"
		)

		self.helpers.test_profile_pic_added(token=token)

		# Add 2nd Profile pic: doesn an update, filename stays the same:
		file3 = open('/Users/glenn/Documents/GettingMEAN/my_loc8r/tests/profile_pic/bug2.png', 'rb')

		profile1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'userprofile']), 
			data=None,
			auth=(token, str(None)), 
			files={'file': file3},
			expected_status_code=200, 
			descriptive_error_msg="success, add second profile pic"
		)

		self.helpers.test_profile_pic_added(token=token)	



		# clean up:
		self.helpers.test_remove_pic(token=token)	

		
		file1.close()
		file2.close()
		file3.close()


	def test_profile_pic_01(self):
		'''
		
		tests for GET:/api/profile/<userid>.

		this endpoint is used to get a profile pic of the user.  If no pic is
		found for the user than a default silhouette is sent.

		'''

		# Set up 2 users. User 1 supplies a profile pic and user 2 does not:

		self.helpers.reset_users_collection()

		# Add User 1: success:
		register1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'register']), 
			data={
				'name': "Madison Voorhees",
				'email': 'mvoorhees15@hotmail.com',
				'password': 'mABC123'			
			}, 
			auth=None, 
			expected_status_code=201, 
			descriptive_error_msg="registration success"
		)
		
		self.assertTrue('token' in register1_r.json().keys())


		token = register1_r.json()['token']

		# profile pic data:
		file1 = open('/Users/glenn/Documents/GettingMEAN/my_loc8r/tests/profile_pic/bug1.png', 'rb')
		profile1 = {'file': file1}

		# Add user 1 profile pic: success:
		profile1_r = endpoint_test(
			method='POST', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'userprofile']), 
			data=None,
			auth=(token, str(None)), 
			files=profile1,
			expected_status_code=200, 
			descriptive_error_msg="success, add first profile pic"
		)

		self.helpers.test_profile_pic_added(token=token)

		file1.close()

		user1_data = self.helpers.decode_token(token=token)

		# print(user1_data)

		# get user 1's profile pic: success:
		profile1_r = endpoint_test(
			method='GET', 
			scheme=self.scheme, 
			url=self.url, 
			endpoint='/'.join(['api', 'profile', user1_data['_id']]), 
			data=None,
			auth=None, 
			files=None,
			expected_status_code=200, 
			descriptive_error_msg="success, receive user pic"
		)





if __name__ == '__main__':
	unittest.main()


































