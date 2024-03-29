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
# from dotenv import load_dotenv
# import os


import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class APIEndPointTests(object):
	'''
	
	Runs common tests for an API end point.


	'''


	def __init__(self, scheme, url, method, endpoint, auth, decode_key, parent_id, child_id, data, status_codes=None):
		'''


		'''

		self._scheme = scheme
		self._url = url
		self._method = method
		self._endpoint = endpoint
		self._auth = auth
		self._decode_key = decode_key
		self._parent_id = parent_id
		self._child_id = child_id
		self._data = data


		'''


		'''

		self._status_codes = {
			"no_auth_parentid_none": 404,
			"no_auth_parentid_invalid": 400,
			"no_auth_parentid_not_found": 404,

			"auth_parentid_none": 405,
			# "auth_parentid_none": 404,
			"auth_parentid_invalid": 400,
			"auth_parentid_not_found": 404,

			# "auth_required_parentid_none": 404,
			# "auth_required_parentid_invalid": 400,
			# "auth_required_parentid_not_found": 404,

			"auth_required_parentid_none": 405,
			# "auth_required_parentid_none": 401,
			"auth_required_parentid_invalid": 401,
			"auth_required_parentid_not_found": 401,



			"no_auth_childid_none": 404,
			"no_auth_childid_invalid": 400 ,
			"no_auth_childid_not_found": 404,

			"auth_childid_none": 404,
			"auth_childid_invalid": 400,
			"auth_childid_not_found": 404,

			# "auth_required_childid_none": 404,
			# "auth_required_childid_invalid": 400,
			# "auth_required_childid_not_found": 404,

			"auth_required_childid_none": 405,
			"auth_required_childid_invalid": 401,
			"auth_required_childid_not_found": 401,

			"no_auth_post_invalid": 405,
			"no_auth_get_invalid": 405,
			"no_auth_put_invalid": 405,
			"no_auth_delete_invalid": 405,

			"auth_post_invalid": 405,
			"auth_get_invalid": 405,
			"auth_put_invalid": 405,
			"auth_delete_invalid": 405 ,

			# "auth_required_post_invalid": 404,
			# "auth_required_get_invalid": 405,
			# "auth_required_put_invalid": 405,
			# "auth_required_delete_invalid": 405,

			"auth_invalid_token": 401,
			"auth_expired_token": 401,
		}

		# can update an error code but supplying the error_codes argument.
		# This will update the default error codes as required.

		if isinstance(status_codes, dict):
			for test, new_status_code in status_codes.items():
				self._status_codes[test] = new_status_code


	def run_tests(self):
		'''

		'''

		if self._parent_id:
			self.parent_id_endpoint_tests()
		
		if self._child_id:
			self.child_id_endpoint_tests()

		self.invalid_methods_tests()

		# self.data_tests()

		if self._auth:
			self.authorization_tests()


	def parent_id_endpoint_tests(self):
		'''

		'''

		parent_ids = {
			'parentid_invalid': self._parent_id[1:],
			'parentid_not_found': str(ObjectId()),
			'parentid_none': None,
		}


		descriptive_error_msgs = {
			'parentid_invalid': "parentid invalid",
			'parentid_not_found': "parentid not found",
			'parentid_none': "no parentid"
		}

		if self._auth:
			for parent_key, parent_id in parent_ids.items():

				if parent_key == 'parentid_invalid':
					auth_test_status_code = self._status_codes['auth_parentid_invalid']
					auth_required_test_status_code = self._status_codes['auth_required_parentid_invalid']


				elif parent_key == 'parentid_not_found':
					auth_test_status_code = self._status_codes['auth_parentid_not_found']
					auth_required_test_status_code = self._status_codes['auth_required_parentid_not_found']


				elif parent_key == 'parentid_none':
					auth_test_status_code = self._status_codes['auth_parentid_none']
					auth_required_test_status_code = self._status_codes['auth_required_parentid_none']

		
				# end point test with authorization:
				endpoint_test(
					scheme=self._scheme,
					url=self._url,
					method=self._method,					
					endpoint=self.build_parent_id_endpoint(parent_id=parent_id), 
					data=self._data, 
					auth=self._auth,
					expected_status_code=auth_test_status_code,
					descriptive_error_msg=descriptive_error_msgs[parent_key]
				)


				# end point test without authorization:
				endpoint_test(
					scheme=self._scheme,
					url=self._url,
					method=self._method,					
					endpoint=self.build_parent_id_endpoint(parent_id=parent_id), 
					data=self._data, 
					auth=(str(None), str(None)),
					expected_status_code=auth_required_test_status_code,
					descriptive_error_msg=descriptive_error_msgs[parent_key]
				)

		else:


			for parent_key, parent_id in parent_ids.items():

				# print("parent_key = {}".format(parent_id))

				if parent_key == 'parentid_invalid':
					no_auth_test_status_code = self._status_codes['no_auth_parentid_invalid']

				elif parent_key == 'parentid_not_found':
					no_auth_test_status_code = self._status_codes['no_auth_parentid_not_found']

				elif parent_key == 'parentid_none':
					no_auth_test_status_code = self._status_codes['no_auth_parentid_none']


				# print("self.build_parent_id_endpoint(parent_id=parent_id) = {}".format(self.build_parent_id_endpoint(parent_id=parent_id)))

				endpoint_test(
					scheme=self._scheme,
					url=self._url,
					method=self._method,
					endpoint=self.build_parent_id_endpoint(parent_id=parent_id), 
					data=self._data, 
					auth=None,
					expected_status_code=no_auth_test_status_code,
					descriptive_error_msg=descriptive_error_msgs[parent_key]
				)



		# returning self so can chain test methods when ran individually
		return self


	def child_id_endpoint_tests(self):
		'''

		'''

		child_ids = {
			'childid_invalid': self._child_id[1:],
			'childid_not_found': str(ObjectId()),
			'childid_none': None,
		}

		
		descriptive_error_msgs = {
			'childid_invalid': "childid invalid",
			'childid_not_found': "childid not found",
			'childid_none': "no childid"
		}



		if self._auth:

			for child_key, child_id in child_ids.items():
				if child_key == 'childid_invalid':
					auth_test_status_code = self._status_codes['auth_childid_invalid']
					auth_required_test_status_code = self._status_codes['auth_required_childid_invalid']


				elif child_key == 'childid_not_found':
					auth_test_status_code = self._status_codes['auth_childid_not_found']
					auth_required_test_status_code = self._status_codes['auth_required_childid_not_found']


				elif child_key == 'childid_none':
					auth_test_status_code = self._status_codes['auth_childid_none']
					auth_required_test_status_code = self._status_codes['auth_required_childid_none']


		
				# end point test with authorization:
				endpoint_test(
					scheme=self._scheme,
					url=self._url,
					method=self._method,					
					endpoint=self.build_child_id_endpoint(child_id=child_id), 
					data=self._data, 
					auth=self._auth,
					expected_status_code=auth_test_status_code,
					descriptive_error_msg=descriptive_error_msgs[child_key]
				)


				# end point test without authorization:
				endpoint_test(
					scheme=self._scheme,
					url=self._url,
					method=self._method,					
					endpoint=self.build_child_id_endpoint(child_id=child_id), 
					data=self._data, 
					auth=(str(None), str(None)),
					expected_status_code=auth_required_test_status_code,
					descriptive_error_msg=descriptive_error_msgs[child_key]
				)

		else:

			for child_key, child_id in child_ids.items():

				if child_key == 'childid_invalid':
					no_auth_test_status_code = self._status_codes['no_auth_childid_invalid']

				elif child_key == 'childid_not_found':
					no_auth_test_status_code = self._status_codes['no_auth_childid_not_found']

				elif child_key == 'childid_none':
					no_auth_test_status_code = self._status_codes['no_auth_childid_none']


				endpoint_test(
					scheme=self._scheme,
					url=self._url,
					method=self._method,
					endpoint=self.build_child_id_endpoint(child_id=child_id), 
					data=self._data, 
					auth=None,
					expected_status_code=no_auth_test_status_code,
					descriptive_error_msg=descriptive_error_msgs[child_key]
				)


		# returning self so can chain test methods when ran individually
		return self



	def invalid_methods_tests(self):
		'''

		'''

		endpoint = self.build_endpoint()


		all_methods = ['POST', 'GET', 'PUT', 'DELETE']

		invalid_methods = [x for x in all_methods if x != self._method]


		for method in invalid_methods:


			if method == "POST":
				auth_test_code = self._status_codes['auth_post_invalid']
				no_auth_test_code = self._status_codes['no_auth_post_invalid']

			elif method == "GET":
				auth_test_code = self._status_codes['auth_get_invalid']
				no_auth_test_code = self._status_codes['no_auth_get_invalid']

			elif method == "PUT":
				auth_test_code = self._status_codes['auth_put_invalid']
				no_auth_test_code = self._status_codes['no_auth_put_invalid']

			elif method == "DELETE":
				auth_test_code = self._status_codes['auth_delete_invalid']
				no_auth_test_code = self._status_codes['no_auth_delete_invalid']



			endpoint_test(
				scheme=self._scheme,
				url=self._url,
				method=method,
				endpoint=endpoint, 
				data=self._data, 
				auth=None,
				expected_status_code=no_auth_test_code,
				descriptive_error_msg="invalid method"
			)


			if self._auth:
				endpoint_test(
					scheme=self._scheme,
					url=self._url,
					method=method,
					endpoint=endpoint, 
					data=self._data, 
					auth=self._auth,
					expected_status_code=auth_test_code,
					descriptive_error_msg="invalid method"
				)

		# returning self so can chain test methods when ran individually
		return self


	def data_tests(self):
		'''


		'''

		# verify data
		# missing require data
		# invalid data 

		pass

	def authorization_tests(self):
		'''

		'''

		# authorization

		token, password = self._auth

		endpoint = self.build_endpoint()

		# invalid token endpoint test:
		endpoint_test(
			scheme=self._scheme,
			url=self._url,
			method=self._method,
			endpoint=endpoint, 
			data=self._data, 
			auth=(self.create_invalid_token(token), password),
			expected_status_code=self._status_codes['auth_invalid_token'],
			descriptive_error_msg="invalid authorization token"
		)


		# expired token endpoint test:
		endpoint_test(
			scheme=self._scheme,
			url=self._url,
			method=self._method,
			endpoint=endpoint, 
			data=self._data, 
			auth=(self.get_expired_token(token), password),
			expected_status_code=self._status_codes['auth_expired_token'],
			descriptive_error_msg="expired authorization token"
		)


		# returning self so can chain test methods when ran individually
		return self


	# ******************************************************************************************************
	# start private methods:

	def build_endpoint(self):
		'''
		

		'''

		if self._parent_id is not None:
			path_parts = [x if x != '<parentid>' else self._parent_id for x in self._endpoint.split('/')]


			if self._child_id is not None:
				path_parts = [x if x != '<childid>' else self._child_id for x in path_parts]
		

			path = '/'.join(s.strip('/') for s in path_parts)


		else:
			path = self._endpoint



		return path 





	def build_parent_id_endpoint(self, parent_id):
		'''
	
		replaces '<parentid>' in the endpoint template with parent_id.

		if '<childid>' is in the template then it's replace with the class
		child_id parameter.

		'''

		path_parts = [x if x != '<parentid>' else parent_id for x in self._endpoint.split('/') ]


		if self._child_id is not None:
			path_parts = [x if x != '<childid>' else self._child_id for x in path_parts]

		# convert None to empty strings:
		path_parts = [x if x else '' for x in path_parts]


		path = '/'.join(s.strip('/') for s in path_parts)


		return path 


	def build_child_id_endpoint(self, child_id):
		'''
		replaces '<childid>' in the endpoint template with child_id.

		Then replaces '<parentid>' in the endpoint template with the class
		parent_id parameter.

		'''

		path_parts = [x if x != '<childid>' else child_id for x in self._endpoint.split('/') ]
		
		# add replace <parentid> with the correct parent_id:
		path_parts = [x if x != '<parentid>' else self._parent_id for x in path_parts]

		# convert None to empty strings:
		path_parts = [x if x else '' for x in path_parts]

		path = '/'.join(s.strip('/') for s in path_parts)

		return path 




	def create_invalid_token(self, token):
		'''

		changes the 5th character in token to either a 0 or a 1.


		'''

		if token[5] == 0:
			new_value = 1 

		else:
			new_value = 0

		# reconstruct the token with the invalid bit:
		invalid_token = token[0:5] + str(new_value) + token[6:] 

		assert len(invalid_token) == len(token)

		return invalid_token


	def get_expired_token(self, token):
		'''


		'''
		user_data = self.decode_token(token=token)
		user_data['exp'] = int((datetime.datetime.utcnow() - datetime.timedelta(days=7)).timestamp())
		
		return jwt.encode(user_data, self._decode_key, algorithm="HS256")


	def decode_token(self, token):
		'''

		'''

		return jwt.decode(token, self._decode_key, algorithms=["HS256"])







	# end private methods:
	# ******************************************************************************************************


#  External methods:

def endpoint_test(method, scheme, url, endpoint, data, auth, expected_status_code, descriptive_error_msg, expected_error_msg=None, params=None, files=None, headers=None):
	'''

	''' 


	def build_url(path):
		'''
		
		helper method for endpoint_test

		'''

		this_url = urlunsplit((scheme, url, path, None, None))


		return this_url 

	'''
	
	Display a summary of the test. 
	Examples:
	Running POST:/api/locations/123/reviews/456 - with authorization - no parentid - expected status code: 404
	Running POST:/api/locations/123/reviews/456 - with authorization - invalid parentid - expected status code: 404
	Running POST:/api/locations/123/reviews/456 - with authorization - non-existing parentid - expected status code: 404
	
	'''


	status_msg = ''
	status_msg += "Running {}:{} - ".format(method, endpoint) 
	
	if auth is None:
		status_msg += "without authorization - "

	else:
		token, password = auth

		if token is None:
			status_msg += "auth required; no auth - "
		
		else:

			status_msg += "with authorization - "

	status_msg += "expected status code: {} - ".format(expected_status_code)
	status_msg += "{}".format(descriptive_error_msg)

	print(status_msg)


	if method == 'POST':

		if isinstance(headers, dict):
			# makes a request using a header. This is the most generic form and was
			# implemented for Bearer authorization:
			this_request = requests.post(
				url=build_url(path=endpoint),
				headers=headers,
				params=params,
				json=data,
				files=files 
			)

		else:
		
			this_request = requests.post(
				url=build_url(path=endpoint),
				auth=auth,
				params=params,
				json=data,
				files=files 
			)


	if method == 'GET':

		this_request = requests.get(
			url=build_url(path=endpoint),
			params=params,
			auth=auth,
		)


	if method == 'PUT':
		
		this_request = requests.put(
			url=build_url(path=endpoint),
			params=params,
			auth=auth,
			json=data 
		)


	if method == 'DELETE':
		
		this_request = requests.delete(
			url=build_url(path=endpoint),
			params=params,
			auth=auth,
		)


	unittest.TestCase().assertEqual(this_request.status_code, expected_status_code)


	return this_request












