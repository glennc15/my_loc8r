import unittest

from bson import ObjectId

from urllib.parse import urlsplit, urlunsplit
# from pymongo import MongoClient
# import pymongo

# import collections

import datetime
import time 

# import tzlocal
import pytz


import requests

# import os

# # from ..components.mongo_repository import MongoRepository
# from components.mongo_repository import MongoRepository
# from components.mongo_records_reader import MongoRecordsReader 


import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class APITests(unittest.TestCase):

	def setUp(self):
		'''


		'''
		self.scheme = 'http'
		self.url = '127.0.0.1:5000/'
		# self.url = 'localhost:3000'


	def build_url(self, path_parts):
		'''


		'''

		# complete url
		path = '/'.join(s.strip('/') for s in path_parts)
		url = urlunsplit((self.scheme, self.url, path, None, None))


		return url 


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

		self.assertEqual(location_r.status_code, 401)


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

		self.assertEqual(r.status_code, 401)


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

		self.assertEqual(r.status_code, 401)

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

		self.assertEqual(r.status_code, 401)


		# DELETE a location:

		# unsuccessful delete, incorrect id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:]])
		r = requests.delete(url=url)
		self.assertEqual(r.status_code, 401)


		# unsuccessful delete, no id:
		url = self.build_url(path_parts=['api', 'locations'])
		r = requests.delete(url=url)
		self.assertEqual(r.status_code, 401)


		# successful delete:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id']])
		r = requests.delete(url=url)
		self.assertEqual(r.status_code, 204)

		



	def read_a_location(self, location_id, expected_reviews=None, expected_rating=None, timedelay=1):
		'''
		
		helper method to CRUD testing

		'''

		# have to add a small delay so rating can update correctly.
		time.sleep(timedelay) 

		url = self.build_url(path_parts=['api', 'locations', location_id])
		location_r = requests.get(url=url)

		self.assertEqual(location_r.status_code, 200)

		if expected_reviews:
			self.assertEqual(len(location_r.json()['reviews']), expected_reviews)

		if expected_rating:
			self.assertEqual(location_r.json()['rating'], expected_rating)


		return location_r




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

		self.assertEqual(review1_r.status_code, 400)


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

		self.assertEqual(review1_r.status_code, 404)


		# CREATE failure due to no rating (rating is a required):
		
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_r = requests.post(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 400)


		
		# CREATE review #1 success:

		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_r = requests.post(
			url=url,
			json={
				'author': 'Simmon Holmes',		
				'rating': "5",
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)

		self.assertEqual(review1_r.status_code, 201)

		# read location and verify the review was added and rating updated:

		location_r = self.read_a_location(
			location_id=location_r.json()['_id'], 
			expected_reviews=1, 
			expected_rating=5, 
		)
		


		# CREATE review #2 success:

		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review2_r = requests.post(
			url=url,
			json={
				'author': 'Charlie Chaplin',		
				'rating': "2",
				'reviewText': "Didn't get any work done, great place!",
			}
		)

		self.assertEqual(review2_r.status_code, 201)

		# read location and verify the review was added and rating updated:

		location_r = self.read_a_location(
			location_id=location_r.json()['_id'], 
			expected_reviews=2, 
			expected_rating=3, 
		)



		# READ a review:

		# READ failure due to incorrect location id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review1_r.json()['_id']])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 404)

		# READ failure due to no location id:
		url = self.build_url(path_parts=['api', 'locations', 'reviews', review1_r.json()['_id']])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 404)


		# READ failure due to incorrect review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id'][1:]])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 404)

		# READ failure due to no review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews'])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 404)
		

		# READ success
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id']])
		review1_err_r = requests.get(url=url)
		self.assertEqual(review1_err_r.status_code, 200)



		# UPDATE a review:

		# UPDATE failure due to incorrect location id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review1_r.json()['_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': "5",
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 404)


		# UPDATE failure due to no location id:
		url = self.build_url(path_parts=['api', 'locations', 'reviews', review1_r.json()['_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': "5",
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 404)

		# UPDATE failure due to incorrect review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id'][1:]])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': "5",
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
				'rating': "5",
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 404)
		
		# UPDATE failure due to no rating (rating is required):
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 404)


		# UPDATE success

		# author needs to be correct from 'Simmon Holmes' to 'Simon Holmes'
		original_review = location_r.json()['reviews'][0]
		self.assertEqual(original_review['author'], 'Simmon Holmes')

		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review1_r.json()['_id']])
		review1_update_r = requests.put(
			url=url,
			json={
				'author': 'Simon Holmes',		
				'rating': "5",
				'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!",
			}
		)
		self.assertEqual(review1_update_r.status_code, 200)

		location_r = self.read_a_location(
			location_id=location_r.json()['_id'], 
			expected_reviews=2, 
			expected_rating=3, 
		)

		updated_review = location_r.json()['reviews'][0]
		self.assertEqual(updated_review['author'], 'Simon Holmes')

		# update the second review's rating to 5
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review2_r.json()['_id']])

		review2_update_r = requests.put(
			url=url,
			json={
				'author': 'Charlie Chaplin',		
				'rating': "5",
				'reviewText': "Didn't get any work done, great place!",
			}
		)

		self.assertEqual(review2_update_r.status_code, 200)

		location_r = self.read_a_location(
			location_id=location_r.json()['_id'], 
			expected_reviews=2, 
			expected_rating=5, 
		)

		# DELETE a review:

		# DELETE failure due to incorrect location id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews', review2_r.json()['_id']])
		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 404)

		# DELETE failure due to no location id:
		url = self.build_url(path_parts=['api', 'locations', 'reviews', review2_r.json()['_id']])
		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 404)
		
		# DELETE failure due to incorrect review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review2_r.json()['_id'][1:]])
		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 404)
		
		# DELETE failure due to no review id:
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'][1:], 'reviews'])
		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 404)
		
		# DELETE success
		url = self.build_url(path_parts=['api', 'locations', location_r.json()['_id'], 'reviews', review2_r.json()['_id']])
		review2_delete_r = requests.delete(url=url)
		self.assertEqual(review2_delete_r.status_code, 204)


		location_r = self.read_a_location(
			location_id=location_r.json()['_id'], 
			expected_reviews=1, 
			expected_rating=5, 
		)




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
		
		for test_record in all_loc_r.json():
			url = self.build_url(path_parts=['api', 'locations', test_record['_id']])
			r = requests.delete(url=url)
			self.assertEqual(r.status_code, 204)


	def test_locations_geoNear_01(self):
		'''


		'''

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
				'maxDistance': 1
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


























