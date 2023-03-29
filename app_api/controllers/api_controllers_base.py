import mongoengine as me
import jwt
from dotenv import load_dotenv
import os

from my_loc8r.app_api.models.location_models import Locations


class APIControllersBase(object):
	'''
	
	Base class for all controllers.


	This class also contains some helper methods that are usefull to all controllers


	'''


	def __init__(self):

		self.status_code = None 
		self.data = None


	@property
	def status_code(self):
		return self._status_code 

	@status_code.setter
	def status_code(self, value):
		self._status_code = value


	@property
	def html(self):
		return self._html 

	@html.setter
	def html(self, value):
		self._html = value

	# data is an alias for html. data makes more since to use in an api.
	@property
	def data(self):
		return self.html 

	@data.setter
	def data(self, value):
		self.html = value


	# *******************************************************************************
	# START: helper methods:		

	def common_validation_errors(self, exception):
		'''


		'''
		if isinstance(exception, me.errors.ValidationError):
			self.data = {'error': "{}".format(exception)}
			self.status_code = 400

		elif isinstance(exception, KeyError):
			self.data = {'error': "{} filed is reqired".format(exception)}
			self.status_code = 400

		elif isinstance(exception, Locations.DoesNotExist):
			self.data = {'error': "No record found. {}".format(exception)}
			self.status_code = 404


		else:
			raise exception 



	def convert_object_ids(self, document):
		'''
		
		Mongo ObjectId cannot be converted to JSON.

		Each Mongoengine Document class has a .to_json() method but it converts
		ObjectIds to {'$oid': '6408a9dcdec8287c6dfd03d6'}
		
		So converts all ObjectId objects to strings

		'''

		if isinstance(document, dict):
			record = document

		else:
			record = document.to_mongo().to_dict()

		# # convert the ObjectId in the location object:
		record['_id'] = str(record['_id'])


		# Convert Location ObjectIds:
		for l_key, l_value in record.items():
			if isinstance(l_value, ObjectId):
				record[l_key] = str(l_value)


		# convert the ObjectId for each opeing time sub document
		for opening_time in record['openingTimes']:
			for o_key, o_value in opening_time.items():
				if isinstance(o_value, ObjectId):
					opening_time[o_key] = str(o_value) 


		# convert the ObjectId for each review sub document
		# pdb.set_trace()
		for review in record['reviews']:
			for r_key, r_value in review.items():
				if isinstance(r_value, ObjectId):
					review[r_key] = str(r_value)



		return record 




	def is_object_id_ok(self, request, object_id):
		'''

		Validate object_id is ObjectId object. Any invalid object_id is a 401 error.


		'''

		if not bson.objectid.ObjectId.is_valid(object_id):

			scheme, netloc, path, query, fragment = urlsplit(request.base_url)

			error_msg = "{} {}{} is not valid\n".format(request.method, path, query)
			error_msg += "{} is not a valid id".format(object_id)

			self.data = {'message': error_msg}
			self.status_code = 404

			return False 

		return True





	def get_location_rating(self, location_obj):
		'''


		'''

		rating = 0

		if len(location_obj.reviews) > 0:
			for review in location_obj.reviews:
				rating += review.rating 

			rating /= len(location_obj.reviews)

			rating = int(rating)

		return rating



	# def build_test_locations(self):
	# 	'''

	# 	'''

	# 	data = [
	# 		{
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
	# 		},
	# 		{
	# 			'name': 'Starcups',
	# 			'address': "125 High Street, Reading, RG6 1PS",
	# 			'facilities': "Hot drinks,Food,Premium wifi",
	# 			'lng': -0.9690884,
	# 			'lat': 51.455061,
	# 			'openingTimes': [
	# 				{
	# 					'days': "Monday - Friday",
	# 					'opening': "7:00am",
	# 					'closing': "5:00pm",
	# 					'closed': False
	# 				},
	# 				{
	# 					'days': "Saturday",
	# 					'opening': "8:00am",
	# 					'closing': "5:00pm",
	# 					'closed': False
	# 				},
	# 				{
	# 					'days': "Sunday",
	# 					'closed': True
	# 				},
	# 			]
	# 		},
	# 		{        
	# 			'name': 'Cafe Hero',
	# 			'address': "555 High Street, Reading, RG6 1PS",
	# 			'facilities': "Hot drinks,Premium wifi",
	# 			'lng': -0.9690964,
	# 			'lat': 51.455051,
	# 			'openingTimes': [
	# 				{
	# 					'days': "Monday - Friday",
	# 					'opening': "7:00am",
	# 					'closing': "10:00pm",
	# 					'closed': False
	# 				},
	# 				{
	# 					'days': "Saturday",
	# 					'closed': True
	# 				},
	# 				{
	# 					'days': "Sunday",
	# 					'closed': True
	# 				},
	# 			],
	# 		}
	# 	]

	# 	# add the location data with POST requests to the api:
	# 	url = self.build_url(path_parts=['api', 'locations'])

	# 	response_json = list()

	# 	for record in data:
	# 		r = requests.post(url=url, json=record)

	# 		if r.status_code != 201:
	# 			print("Error writing data")
	# 			raise ValueError("There was a problem with the POST request for {}".format(record['name']))

	# 		response_json.append(r.json())


	# 	return response_json



	# def remove_all_records(self):
		# '''


		# '''

		# url = self.build_url(path_parts=['api', 'locations'])

		# try:
		# 	all_loc_r = requests.get(
		# 		url=url,
		# 		params={
		# 			'lng': 1,
		# 			'lat': 1,
		# 			'maxDistance': 100000000
		# 		}
		# 	)


		# 	# test_records = all_loc_r.json()

		# 	# print(test_records)

		# 	# pdb.set_trace()
			
		# 	for test_record in all_loc_r.json():
		# 		url = self.build_url(path_parts=['api', 'locations', test_record['_id']])
		# 		r = requests.delete(url=url)
		# 		try:
		# 			self.assertEqual(r.status_code, 204)

		# 		except Exception as e:
		# 			print("url = {}".format(url))
		# 			print("test_record['_id'] = {}".format(test_record['_id']))
		# 			raise e

		# except Exception as e:
		# 	pass 


	# def drop_db(self):
	# 	'''

	# 	'''

	# 	APITests.mongo_client.drop_database(self.db_name)

		

	# def build_url(self, path_parts):
	# 	'''


	# 	'''

	# 	# complete url
	# 	path = '/'.join(s.strip('/') for s in path_parts)
	# 	url = urlunsplit((self.scheme, self.url, path, None, None))


	# 	return url 

	# def location_tests(self, location_id, expected_reviews, expected_rating):
	# 	'''

	# 	'''

	# 	# print("location_id = {}".format(location_id))

	# 	# print("location_id = {}".format(location_id))
	# 	# pdb.set_trace()

	# 	db_location = APITests.mongo_client[self.db_name]['locations'].find_one({'_id': ObjectId(location_id)})

	# 	self.assertEqual(db_location['rating'], expected_rating)
		
	# 	# for whatever reason when all reviews are removed the location
	# 	# ['reviews'] no longer exists in the database. But can add another
	# 	# reviews without issues. When another review is added then location
	# 	# ['reviews'] is present again.

	# 	if db_location.get('reviews'):
	# 		self.assertEqual(len(db_location['reviews']), expected_reviews)

	# 	else:
	# 		self.assertEqual(0, expected_reviews)


	# def add_test_location(self, reviews):
	# 	'''
		
	# 	Adds a test location and up to 2 reviews each with a unique user:

	# 	'''

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



	# 	if reviews == 0:
	# 		return (location_id)

	# 	elif (reviews==1) or (reviews==2):

	# 		# Review 1 / User 1
	# 		register1_r = requests.post(
	# 			url=self.build_url(path_parts=['api', 'register']),
	# 			json={
	# 				'name': "Madison Voorhees",
	# 				'email': 'mvoorhees@hotmail.com',
	# 				'password': 'mABC123'
	# 			}
	# 		)

	# 		self.assertEqual(register1_r.status_code, 201)		
	# 		self.assertTrue('token' in register1_r.json().keys())

	# 		user1_token = register1_r.json()['token']


	# 		review1_r = requests.post(
	# 			url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 			auth=(user1_token, str(None)),
	# 			json={
	# 				'rating': 5,		
	# 				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
	# 			}
	# 		)

	# 		review1_id = review1_r.json()['_id']

	# 		self.assertEqual(review1_r.status_code, 201)
	# 		self.assertEqual(review1_r.json()['author'], 'Madison Voorhees')
	# 		self.assertEqual(review1_r.json()['rating'], 5)
	# 		self.assertEqual(review1_r.json()['review_text'], 'No wifi. Has male and female a go-go dances. Will be back with the family!')

	# 		self.location_tests(
	# 			location_id=location_id, 
	# 			expected_reviews=1, 
	# 			expected_rating=5, 
	# 		)

	# 		if reviews == 1:
	# 			return (location_id, review1_id, user1_token)


	# 		# Review 2/ User 2:
	# 		register2_r = requests.post(
	# 			url=self.build_url(path_parts=['api', 'register']),
	# 			json={
	# 				'name': "Simon Hardy",
	# 				'email': 'mhardy@hotmail.com',
	# 				'password': 'sABC123'
	# 			}
	# 		)

	# 		self.assertEqual(register2_r.status_code, 201)		
	# 		self.assertTrue('token' in register1_r.json().keys())

	# 		user2_token = register2_r.json()['token']


	# 		review2_r = requests.post(
	# 			url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
	# 			auth=(user2_token, str(None)),
	# 			json={	
	# 				'rating': 2,
	# 				'reviewText': "Didn't get any work done, great place!",
	# 			}
	# 		)

	# 		review2_id = review2_r.json()['_id']
			
	# 		self.assertEqual(review2_r.status_code, 201)
	# 		self.assertEqual(review2_r.json()['author'], 'Simon Hardy')
	# 		self.assertEqual(review2_r.json()['rating'], 2)
	# 		self.assertEqual(review2_r.json()['review_text'], "Didn't get any work done, great place!")


	# 		self.location_tests(
	# 			location_id=location_id, 
	# 			expected_reviews=2, 
	# 			expected_rating=3, 
	# 		)

	# 		return (location_id, review1_id, user1_token, review2_id, user2_token)


	# 	else:

	# 		raise ValueError("reviews = {} is not valid. 0 <= reviews <= 2".format(reviews))


	# def reset_users_collection(self):
	# 	'''

	# 	'''

	# 	# drop users collection and recreate it with a unique index for email:
	# 	APITests.mongo_client[self.db_name].drop_collection('users')
	# 	APITests.mongo_client[self.db_name].create_collection('users')
	# 	APITests.mongo_client[self.db_name]['users'].create_index('email', unique=True)

		
	# def reset_locations_collection(self):
	# 	'''

	# 	'''

	# 	# drop users collection and recreate it with a unique index for email:
	# 	APITests.mongo_client[self.db_name].drop_collection('locations')
	# 	APITests.mongo_client[self.db_name].create_collection('locations')
	# 	APITests.mongo_client[self.db_name]['locations'].create_index([('coords', pymongo.GEOSPHERE)])


	def decode_token(self, token):
		'''

		'''
		load_dotenv()

		return jwt.decode(token, self._encode_key, algorithms=["HS256"])





	# End: helper methods:
	# *******************************************************************************











	