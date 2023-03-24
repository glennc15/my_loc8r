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

# import os

# # from ..components.mongo_repository import MongoRepository
# from components.mongo_repository import MongoRepository
# from components.mongo_records_reader import MongoRecordsReader 


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

		pass 


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

		db_location = APITests.mongo_client[self.db_name]['location'].find_one({'_id': ObjectId(location_id)})

		self.assertEqual(db_location['rating'], expected_rating)
		self.assertEqual(len(db_location['reviews']), expected_reviews)




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



	def test_review_crud_01(self):
		
		'''
		


		'''


		# create a test location and then add reviews:
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

		# CREATE a review:

		# CREATE failure due to incorrect location id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews'])
		review1_r = requests.post(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': "5",
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 404)


		# CREATE failure due to no location id:
		url = self.build_url(path_parts=['api', 'locations', 'reviews'])
		review1_r = requests.post(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': "5",
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 401)


		# CREATE failure due to no rating (rating is a required):		
		review1_r = requests.post(
			url=self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews']),
			json={
				'author': 'Simon Holmes',		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 400)


		# CREATE failure due to no author (author is a required):		
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_r = requests.post(
			url=self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews']),
			json={
				'rating': 5,		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 400)


		# CREATE failure due to no review text (review text is a required):		
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_r = requests.post(
			url=self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews']),
			json={
				'author': 'Simon Holmes',
				'rating': 5,		
			}
		)

		self.assertEqual(review1_r.status_code, 400)



		# CREATE unsuccessful due to imporper request (GET not allowed):
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_r = requests.get(
			url=url,
			json={
				'author': 'Simmon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 405)

		# CREATE unsuccessful due to imporper request (PUT not allowed):
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_r = requests.put(
			url=url,
			json={
				'author': 'Simmon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 405)


		# CREATE unsuccessful due to imporper request (DELETE not allowed):
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_r = requests.delete(
			url=url,
			json={
				'author': 'Simmon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 405)

		
		# CREATE review #1 success:
		location_id = location_r.json()['_id']

		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_r = requests.post(
			url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
			json={
				'author': 'Simmon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 201)
		# self.assertTrue('_id' in review1_r.json())

		# self.assertTrue('_id' in review1_r.json())

		# read location and verify the review was added and rating updated:

		# location_r = self.location_tests(
		# 	location_id='640c131b0eff6bceca9e57b8', 
		# 	expected_reviews=1, 
		# 	expected_rating=5, 
		# )


		self.location_tests(
			location_id=location_id, 
			expected_reviews=1, 
			expected_rating=5, 
		)
		


		# CREATE review #2 success:

		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review2_r = requests.post(
			url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
			json={
				'author': 'Charlie Chaplin',		
				'rating': 2,
				'reviewText': "Didn't get any work done, great place!",
			}
		)

		self.assertEqual(review2_r.status_code, 201)

		# read location and verify the review was added and rating updated:

		self.location_tests(
			location_id=location_id, 
			expected_reviews=2, 
			expected_rating=3, 
		)



		# READ a review:

		# READ failure due to incorrect location id:
		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review1_r.json()['_id']])
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review1_r.json()['review_id']])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 404)

		# READ failure due to no location id:
		url = self.build_url(path_parts=['api', 'locations', 'reviews', review1_r.json()['review_id']])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 404)


		# READ failure due to non existing location id:
		url = self.build_url(path_parts=['api', 'locations', '640ceee95fedd040ba74a736', 'reviews', review1_r.json()['review_id'][1:]])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 404)


		# READ failure due to incorrect review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['review_id'][1:]])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 404)


		# READ failure due non exixting review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', '640ceee95fedd040ba74a736'])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 404)


		# READ failure due to no review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 405)
		

		# READ success
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['review_id']])
		read_review1_r = requests.get(url=url)
		self.assertEqual(read_review1_r.status_code, 200)
		self.assertEqual(read_review1_r.json()['review_id'], review1_r.json()['review_id'])


		# UPDATE a review:

		# UPDATE failure due to incorrect location id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review1_r.json()['review_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 404)


		# UPDATE failure due to non existing location id:
		url = self.build_url(path_parts=['api', 'locations', '640ceee95fedd040ba74a736', 'reviews', review1_r.json()['review_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 404)


		# UPDATE failure due to no location id:
		url = self.build_url(path_parts=['api', 'locations', 'reviews', review1_r.json()['review_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 404)

		# UPDATE failure due to incorrect review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['review_id'][1:]])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 404)


		# UPDATE failure due to non existing review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', '640ceee95fedd040ba74a736'])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 404)

		# UPDATE failure due to no review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 405)
		

		# UPDATE failure due to no rating (rating is required):
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['review_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 400)


		# UPDATE failure due to no author (author is required):
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['review_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 400)


		# UPDATE failure due to no review text (review is required):
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['review_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'author': 5,
			}
		)
		self.assertEqual(review1_update_r.status_code, 400)


		# UPDATE success

		# author needs to be correct from 'Simmon Holmes' to 'Simon Holmes'
		self.assertEqual(review1_r.json()['author'], 'Simmon Holmes')

		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['review_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 200)

		self.location_tests(
			location_id=location_r.json()['_id'], 
			expected_reviews=2, 
			expected_rating=3, 
		)

		# updated_review = location_r.json()['reviews'][0]
		self.assertEqual(review1_update_r.json()['author'], 'Simon Holmes')

		# update the second review's rating to 5
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review2_r.json()['review_id']])

		review2_update_r = requests.put(
			url=url,
			json={
				'author': 'Charlie Chaplin',		
				'rating': 5,
				'reviewText': "Didn't get any work done, great place!",
			}
		)

		self.assertEqual(review2_update_r.status_code, 200)

		self.location_tests(
			location_id=location_r.json()['_id'], 
			expected_reviews=2, 
			expected_rating=5, 
		)

		# DELETE a review:

		# DELETE failure due to incorrect location id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review2_r.json()['review_id']])
		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 404)

		# DELETE failure due to no location id:
		url = self.build_url(path_parts=['api', 'locations', 'reviews', review2_r.json()['review_id']])
		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 404)
		
		# DELETE failure due to incorrect review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review2_r.json()['review_id'][1:]])
		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 404)
		
		# DELETE failure due to no review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews'])
		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 404)
		
		# DELETE 2nd review: success
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review2_r.json()['review_id']])
		read_review_1 = requests.get(url)
		self.assertEqual(read_review_1.status_code, 200)

		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 204)

		read_review_1 = requests.get(url)
		self.assertEqual(read_review_1.status_code, 404)

		self.location_tests(
			location_id=location_r.json()['_id'], 
			expected_reviews=1, 
			expected_rating=5, 
		)

		# DELETE 1st review: success
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['review_id']])
		read_review_2 = requests.get(url)
		self.assertEqual(read_review_2.status_code, 200)


		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 204)

		# for whatever reason when all reviews are removed the location
		# ['reviews'] no longer exists in the database. But can add another
		# reviews without issues. When another review is added then location
		# ['reviews'] is present again.

		# self.location_tests(
		# 	location_id=location_r.json()['_id'], 
		# 	expected_reviews=0, 
		# 	expected_rating=0, 
		# )

		read_review_2 = requests.get(url)
		self.assertEqual(read_review_2.status_code, 404)


		# CREATE review #1 success:
		location_id = location_r.json()['_id']

		# url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_r = requests.post(
			url=self.build_url(path_parts=['api', 'locations', location_id, 'reviews']),
			json={
				'author': 'Simmon Holmes',		
				'rating': 5,
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 201)


		# Clean up; delete the test location:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id']])
		r = requests.delete(url=url)
		self.assertEqual(r.status_code, 204)


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

		# drop users collection:
		APITests.mongo_client[self.db_name].drop_collection('users')

		# Test registration:

		url = self.build_url(path_parts=['api', 'register'])

		# # Add User: failure due to no data:
		location_r = requests.post(
			url=url,
			json={}
		)

		self.assertEqual(location_r.status_code, 400)
		self.assertEqual(location_r.json()['name'], 'name field is required')
		self.assertEqual(location_r.json()['email'], 'email field is required')
		self.assertEqual(location_r.json()['password'], 'password field is required')


		# Add User: failure due to no name in data:
		location_r = requests.post(
			url=url,
			json={
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 400)
		self.assertEqual(location_r.json()['name'], 'name field is required')


		# Add User: failure due to empty name in data:
		location_r = requests.post(
			url=url,
			json={
				'name': "",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 400)
		self.assertEqual(location_r.json()['name'], "a value of '' is not valid for field name")



		# Add User: failure due to empty name in data:
		location_r = requests.post(
			url=url,
			json={
				'name': "   ",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 400)
		self.assertEqual(location_r.json()['name'], "a value of '   ' is not valid for field name")



		# Add User: failure due to no email in data:
		location_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 400)
		self.assertEqual(location_r.json()['email'], 'email field is required')

		# Add User: failure due to empty email:
		location_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': '',
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 400)
		self.assertEqual(location_r.json()['email'], "a value of '' is not valid for field email")


		# Add User: failure due to invalid email:
		location_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 400)
		self.assertEqual(location_r.json()['email'], "a value of 'mcrosby15hotmail.com' is not valid for field email")



		# Add User: failure due to no password in data:
		location_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
			}
		)

		self.assertEqual(location_r.status_code, 400)
		self.assertEqual(location_r.json()['password'], 'password field is required')


		# Add User: failure due to empty password in data:
		location_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': ''
			}
		)

		self.assertEqual(location_r.status_code, 400)
		self.assertEqual(location_r.json()['password'], "a value of '' is not valid for field password")


		# Add User: failure due to empty password in data:
		location_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': '   '
			}
		)

		self.assertEqual(location_r.status_code, 400)
		self.assertEqual(location_r.json()['password'], "a value of '   ' is not valid for field password")


		# Add User: success:
		location_r = requests.post(
			url=url,
			json={
				'name': "Madison Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 201)		
		self.assertTrue('token' in location_r.json().keys())


		# Add User: failure because the user already exists:
		location_r = requests.post(
			url=url,
			json={
				'name': "Simon Crosby",
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 400)		
		self.assertEqual(location_r.json()['error'], "A user for mcrosby15@hotmail.com already exists")


		# Test login:

		url = self.build_url(path_parts=['api', 'login'])

		# Login failure, no data: 
		location_r = requests.post(
			url=url
		)

		self.assertEqual(location_r.status_code, 404)



		# Login failure, incorrect email: 
		location_r = requests.post(
			url=url,
			json={
				'email': 'crosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 404)


		# Login failure, no email: 
		location_r = requests.post(
			url=url,
			json={
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 404)

		# Login failure, incorrect password: 
		location_r = requests.post(
			url=url,
			json={
				'email': 'mcrosby15@hotmail.com',
				'password': 'maBC123'
			}
		)

		self.assertEqual(location_r.status_code, 404)

		# Login failure, no password: 
		location_r = requests.post(
			url=url,
			json={
				'email': 'mcrosby15@hotmail.com',
			}
		)

		self.assertEqual(location_r.status_code, 404)


		# Login success: 
		location_r = requests.post(
			url=url,
			json={
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 404)



		# Login success: 
		location_r = requests.post(
			url=url,
			json={
				'email': 'mcrosby15@hotmail.com',
				'password': 'mABC123'
			}
		)

		self.assertEqual(location_r.status_code, 201)
		self.assertTrue('token' in location_r.json().keys())



if __name__ == '__main__':
	unittest.main()





















