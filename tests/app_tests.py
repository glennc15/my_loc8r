import unittest

from bson import ObjectId

from urllib.parse import urlsplit, urlunsplit
from pymongo import MongoClient
import pymongo

# import collections

import datetime
import time 

# import tzlocal
import pytz


import requests

from bs4 import BeautifulSoup

# import os

# # from ..components.mongo_repository import MongoRepository
# from components.mongo_repository import MongoRepository
# from components.mongo_records_reader import MongoRecordsReader 

from web_scraper.page_scrapers.locations_scraper import LocationsScraper
from web_scraper.page_scrapers.details_scraper import DetailsScraper
from web_scraper.page_scrapers.error_scraper import ErrorScraper



import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class AppTests(unittest.TestCase):

	def setUp(self):
		'''


		'''
		self.scheme = 'http'
		self.url = '127.0.0.1:5000'
		self.use_static_distance = True
		# self.url = 'localhost:3000'

		self.add_test_locations(add_reviews=False, clear_db=True)



	def test_locations_page_01(self):
		'''

		Test the / (homepage) is displaying the correct data for each location.

		'''

		# Expected data:

		# test_data() returns a list of location records.

		# modify each locaiton as follows:
		# keep .name
		# keep .address
		# keep .facilities
		#
		# add .rating=0
		# add .distance=['proper distance string']
		#
		# remove all other tags:
		
		# expected_data = self.get_homepage_expected_data(ratings=0)
		expected_data = self.get_homepage_expected_data(ratings=0, static_distances=self.use_static_distance)


		# get test data by scraping the locations-list page:

		# set up the scraper for the homepage:
		url = self.build_url()
		loc_scraper = LocationsScraper(url=url)

		# modify each location so it has the folling:
		ok_keys = ['name', 'address', 'facilities', 'distance', 'rating']
		test_data = [dict([(k, v) for k, v in loc_record.items() if k in ok_keys]) for loc_record in loc_scraper.scrape()]


		self.locations_page_test(expected_data=expected_data, test_data=test_data)



	def test_details_page_01(self):
		'''


		'''

		# Expected data:

		# test_data() returns a list of location records.

		# modify each locaiton as follows:
		# keep .name
		# keep .address
		# keep .facilities
		# keep .openingTimes
		# add .rating=0
		# 
		#
		# remove all other tags:


		# expected_data = self.get_details_expected_data(ratings=0, num_reviews=0)
		expected_data = self.get_details_expected_data(ratings=0, num_reviews=0)



		# turn the test data list into a dict with key = location name.
		expected_dict = dict([(location['name'], location) for location in expected_data])


		# Verify the data from each details page against the expected data.

		# getting the url for each details page from the homepage. Then test each details page:

		# set up the scrapers for the homepage and details page:
		url = self.build_url()
		loc_scraper = LocationsScraper(url=url)
		details_scraper = DetailsScraper()

		locations = loc_scraper.scrape()
		self.assertTrue(len(locations)>0, msg="No locations for testing. Possible cause of this failure is the scraper cannot find any data on the Locaitons page.")


		for location in locations:
			# build complete url path to each details page:
			details_url = self.build_url(path_parts=location['details_url'].split('/'))

			test_data = details_scraper.scrape(url=details_url)

			# only keep the following keys:
			ok_keys = ['name', 'address', 'facilities', 'openingTimes', 'rating', 'reviews']
			test_data = dict([(k, v) for k, v in test_data.items() if k in ok_keys])

			
			err_msg_tag = "location-info['{}']".format(location['name'])

			self.compare_data_objs(
				expected_data=expected_dict[test_data['name']],
				test_data=test_data,
				err_msg_tag=err_msg_tag
			)


	def test_details_page_02(self):
		'''
		
		Tests for detail errors such as 404.

		'''

		# Check for a details 404 error. This can occur when the details page
		# an invalid record id:

		# Scrape the normal details page:

		expected_details_data1 = {
			'name': "404, page not found",
			'address': None,
			'rating': None,
			'facilities': None,
			'add_review_url': None,
			'reviews': list(),
			'openingTimes': list()
		}

		details_scraper = DetailsScraper()

		invalid_details_url = self.build_url(path_parts=['location', '6401b4c408c1d613f89439ed'])

		details_test_data1 = details_scraper.scrape(
			url=invalid_details_url,
			expected_status_code=404
		)

		err_msg_tag = "location-info"
		self.compare_data_objs(
			expected_data=expected_details_data1,
			test_data=details_test_data1,
			err_msg_tag=err_msg_tag
		)

		# Scrape the details error page:

		expected_details_data2 = {
			'title': "404, page not found",
			'msg': "Oh dear. Looks like we can't find this page. Sorry.",
		}


		error_scraper = ErrorScraper()
		details_test_data2 = error_scraper.scrape(
			url=invalid_details_url,
			expected_status_code=404
		)

		err_msg_tag = "error"

		self.compare_data_objs(
			expected_data=expected_details_data2,
			test_data=details_test_data2,
			err_msg_tag=err_msg_tag
		)



	def test_add_reviews_01(self):
		'''

		add a review for each location. Then scrape the homepage and each
		details page to ensure each location updated properly.

		'''
		### ADD 1 REVIEW:

		# 1) Get the data for the reviews (author, rating, text). The review
		# data is part of the test data.
		ok_keys = ['name', 'reviews']

		# trim the keys:
		review_data = [dict([(k, v) for k, v in loc_record.items() if k in ok_keys]) for loc_record in self.get_test_data()]
		reviews_dict = dict([(loc['name'], loc) for loc in review_data])

		# the homepage has to be visited first to get the links to each
		# location details page. Then the "add review" link on each details
		# page will be used to get to the location-review-form page.

		# set up the scrapers for the homepage and details page:
		url = self.build_url()
		loc_scraper = LocationsScraper(url=url)
		details_scraper = DetailsScraper()
		# add_review_scraper = AddReviewScraper()

		for location in loc_scraper.scrape():
			# build complete url path to each locations's details page:
			details_url = self.build_url(path_parts=location['details_url'].split('/'))
			loc_detail_data = details_scraper.scrape(url=details_url)

			add_review_url = self.build_url(path_parts=loc_detail_data['add_review_url'].split('/'))

			# not scraping the location-review-form because in this case it's
			# very simple and does not require any hidden data to be
			# submitted with the form.

			# Add the first review for each location::
			this_review = reviews_dict[loc_detail_data['name']]['reviews'][0]

			post_data = {
				'name': this_review['author'],
				'rating': this_review['rating'],
				'review': this_review['reviewText']
			}

			# print("add_review_url = {}".format(add_review_url))
			# pdb.set_trace()

			# The server redirects after a successful post. So checking for
			# the redirect. If the request followed the redirect the status
			# code would be 200.
			post_r = requests.post(
				url=add_review_url,
				json=post_data,
				allow_redirects=False
			)

			self.assertEqual(post_r.status_code, 302)

		### Test 1 REVIEW:

		# Test the / (homepage) is displaying the correct data for each
		# location after adding 1 review for each location. The only thing
		# different on the homepage is the rating. The location rating is the
		# averge of all the location review ratings. The 1st review rating
		# for all locations is 5.

		loc_expected_data1 = self.get_homepage_expected_data(ratings=5)
		
		# scrape the locations data from the locations-list (homepage) page:
		ok_keys = ['name', 'address', 'facilities', 'distance', 'rating']
		locations = loc_scraper.scrape()
		loc_test_data1 = [dict([(k, v) for k, v in loc_record.items() if k in ok_keys]) for loc_record in locations]

		self.locations_page_test(expected_data=loc_expected_data1, test_data=loc_test_data1)


		# Test each location details page has 1 review and the correct rating:
		details_expected_data1 = self.get_details_expected_data(ratings=5, num_reviews=1)
		# turn the test data list into a dict with key = location name.
		details_expected_dict1 = dict([(loc['name'], loc) for loc in details_expected_data1])


		for location in locations:

			# build complete url path to each details page:
			details_url = self.build_url(path_parts=location['details_url'].split('/'))

			details_test_data1 = details_scraper.scrape(url=details_url)

			# only keep the following keys:
			ok_keys = ['name', 'address', 'facilities', 'openingTimes', 'rating', 'reviews']
			details_test_data1 = dict([(k, v) for k, v in details_test_data1.items() if k in ok_keys])


			# Test the details page (but this does not test the reviews)
			self.compare_data_objs(
				expected_data=details_expected_dict1[details_test_data1['name']],
				test_data=details_test_data1,
				err_msg_tag="location-info['{}']".format(location['name'])
			)	

			# Test the reviews (only 1 review:
			self.compare_data_objs(
				expected_data=details_expected_dict1[location['name']]['reviews'][0],
				test_data=details_test_data1['reviews'][0],
				err_msg_tag="location-info['{}']['reviews']".format(location['name'])
			)


		### ADD 2nd REVIEW:
		for location in locations:
			# build complete url path to each details page:
			details_url = self.build_url(path_parts=location['details_url'].split('/'))
			loc_detail_data = details_scraper.scrape(url=details_url)

			add_review_url = self.build_url(path_parts=loc_detail_data['add_review_url'].split('/'))

			# not scraping the location-review-form because in this case it's
			# very simple and does not require any hidden data to be
			# submitted with the form.

			# second review:
			this_review = reviews_dict[loc_detail_data['name']]['reviews'][1]

			post_data = {
				'name': this_review['author'],
				'rating': this_review['rating'],
				'review': this_review['reviewText']
			}


			# The server redirects after a successful post. So checking for
			# the redirect. If the request followed the redirect the status
			# code would be 200.
			post_r = requests.post(
				url=add_review_url,
				json=post_data,
				allow_redirects=False
			)

			self.assertEqual(post_r.status_code, 302)

		### Test All Reviews:

		# Test the / (homepage) is displaying the correct data for each
		# location after adding 2 reviews for each location. The only thing
		# different on the homepage is the rating. The location rating is the
		# averge of all the location review ratings.

		ratings = {
			'Starcups': 4,
			'Cafe Hero': 3,
			"Burger Queen": 4
		}

		loc_expected_data2 = self.get_homepage_expected_data(ratings=ratings)
		

		# modify each location so it has the folling:
		ok_keys = ['name', 'address', 'facilities', 'distance', 'rating']
		locations = loc_scraper.scrape()
		loc_test_data2 = [dict([(k, v) for k, v in loc_record.items() if k in ok_keys]) for loc_record in locations]

		self.locations_page_test(expected_data=loc_expected_data2, test_data=loc_test_data2)

		# Test each location details page has 2 reviews and he correct rating:
		details_expected_data2 = self.get_details_expected_data(ratings=ratings, num_reviews=2)

		# turn the details test data list into a dict with key = location name.
		details_expected_dict2 = dict([(loc['name'], loc) for loc in details_expected_data2])


		for location in locations:

			# scrape the details page and prepare the data:
			details_url = self.build_url(path_parts=location['details_url'].split('/'))
			details_test_data2 = details_scraper.scrape(url=details_url)

			# only keep the following details data:
			ok_keys = ['name', 'address', 'facilities', 'openingTimes', 'rating', 'reviews']
			details_test_data2 = dict([(k, v) for k, v in details_test_data2.items() if k in ok_keys])


			# Test the details page (but this does not test the reviews)
			self.compare_data_objs(
				expected_data=details_expected_dict2[details_test_data2['name']],
				test_data=details_test_data2,
				err_msg_tag="location-info['{}']".format(location['name'])
			)	

			# test all the reviews on the details page:

			expected_reviews = sorted(details_expected_dict2[details_test_data2['name']]['reviews'], key=lambda x: x['author'])
			test_reviews = sorted(reviews_dict[location['name']]['reviews'], key=lambda x: x['author'])

			for expectd_review, test_review in zip(expected_reviews, test_reviews):

				self.compare_data_objs(
					expected_data=expectd_review,
					test_data=test_review,
					err_msg_tag="location-info['{}']['reviews']".format(location['name'])
				)


	def test_add_reviews_validation_01(self):
		'''

		add a review with missing data and check for proper validation.

		'''

		# set up the scrapers for the homepage and details page:
		url = self.build_url()
		loc_scraper = LocationsScraper(url=url)
		details_scraper = DetailsScraper()
		# add_review_scraper = AddReviewScraper()
		err_scraper = ErrorScraper()

		# have to follow the links to the review page to ensure proper
		# location ids in the url:

		loc_data = loc_scraper.scrape()


		# build complete url path to the first location page: 
		details_url = self.build_url(path_parts=loc_data[0]['details_url'].split('/'))
		loc_detail_data = details_scraper.scrape(url=details_url)

		add_review_url = self.build_url(path_parts=loc_detail_data['add_review_url'].split('/'))

		# # all data missing:
		# post_data = {
		# 	'name': None,
		# 	'rating': None,
		# 	'review': None
		# }

		# Test with no data:


		post_r = requests.post(
			url=add_review_url,
			json={},
			allow_redirects=False
		)

		self.assertEqual(post_r.status_code, 400)

		expected_error_data1 = {
			'title': "400, something's gone wrong",
			'msg': "Something, somewhere, has gone just a little bit wrong.",
		}


		err_scraper.html = post_r.text

		test_error_data1 = err_scraper.scrape(read_site=False)
		
		self.compare_data_objs(
			expected_data=expected_error_data1,
			test_data=test_error_data1,
			err_msg_tag='error-page'
		)


		# Test with missing author:
		post_data = {
			'name': None,
			'rating': 2,
			'review': "Not a good review"
		}

		post_r = requests.post(
			url=add_review_url,
			json=post_data,
			allow_redirects=False
		)

		self.assertEqual(post_r.status_code, 400)

		expected_error_data1 = {
			'title': "400, something's gone wrong",
			'msg': "Something, somewhere, has gone just a little bit wrong.",
		}

		err_scraper.html = post_r.text
		test_error_data1 = err_scraper.scrape(read_site=False)
		
		self.compare_data_objs(
			expected_data=expected_error_data1,
			test_data=test_error_data1,
			err_msg_tag='error-page'
		)



		# Test with missing rating:
		post_data = {
			'name': "Glenn",
			'rating': None,
			'review': "Not a good review"
		}

		post_r = requests.post(
			url=add_review_url,
			json=post_data,
			allow_redirects=False
		)

		self.assertEqual(post_r.status_code, 400)

		expected_error_data1 = {
			'title': "400, something's gone wrong",
			'msg': "Something, somewhere, has gone just a little bit wrong.",
		}

		err_scraper.html = post_r.text
		test_error_data1 = err_scraper.scrape(read_site=False)
		
		self.compare_data_objs(
			expected_data=expected_error_data1,
			test_data=test_error_data1,
			err_msg_tag='error-page'
		)


		# Test with missing review:
		post_data = {
			'name': "Glenn",
			'rating': 2,
			'review': None
		}

		post_r = requests.post(
			url=add_review_url,
			json=post_data,
			allow_redirects=False
		)

		self.assertEqual(post_r.status_code, 400)

		expected_error_data1 = {
			'title': "400, something's gone wrong",
			'msg': "Something, somewhere, has gone just a little bit wrong.",
		}

		err_scraper.html = post_r.text
		test_error_data1 = err_scraper.scrape(read_site=False)
		
		self.compare_data_objs(
			expected_data=expected_error_data1,
			test_data=test_error_data1,
			err_msg_tag='error-page'
		)




	# *********************************************************************************
	#  Start Helper Methods:

	def get_homepage_expected_data(self, ratings=0, static_distances=False):
		'''

		ratings=[number]: sets the rating for all locations = number.

		ratings={
			'Starcups': num1,
			'Cafe Hero': num2
		}

			sets a differecnt rating for each location.

		'''

		ok_keys = ['name', 'address', 'facilities']

		# trim the keys:
		expected_data = [dict([(k, v) for k, v in loc_record.items() if k in ok_keys]) for loc_record in self.get_test_data()]
	
		# Set the ratings:
		if isinstance(ratings, dict):
			expected_data = [dict(**loc, rating=ratings[loc['name']]) for loc in expected_data]
			

		else:	
			expected_data = [dict(**loc, rating=ratings) for loc in expected_data]

		# add expected distances to each location: 

		# turn the test data list into a dict with key = location name. This
		# will make it easier to add distances to the correct record.
		expected_dict = dict([(location['name'], location) for location in expected_data])

		if static_distances:
			expected_dict['Starcups']['distance'] = '6m'
			expected_dict['Cafe Hero']['distance'] = '62m'
			expected_dict['Burger Queen']['distance'] = '1.1km'

		else:
			# have to get distances from the api and convert the distance to the
			# correct string

			url = self.build_url(path_parts=['api', 'locations'])
			location_r = requests.get(
				url=url,
				params={
					'lng': -0.9690885,
					'lat': 51.455041,
					'maxDistance': 20
				}
			)

			self.status_code_test(
				url=url,
				expected_status_code=200,
				test_status_code=location_r.status_code
			)

			for location in location_r.json():
				
				# print("location = {}".format(location))

				if location.get('distance'):
					distance = location['distance']

				else:
					distance = location['dist_calc']
					

				if distance < 1.0:
					distance_str = "{}m".format(int(distance*1000))

				else:
					distance_str = "{:.1f}km".format(distance)

				expected_dict[location['name']]['distance'] = distance_str


		# convert expected_dict back to a list:
		expected_data = [location for name, location in expected_dict.items()]

		return expected_data

	def get_details_expected_data(self, ratings=0, num_reviews=0):
		'''
		
		ratings:
			ratings=[number]: sets the rating for all locations = number.

			ratings={
				'Starcups': num1,
				'Cafe Hero': num2
			}

			sets a different rating for each location.

		reviews:
			sets the number of reviews to return.

		'''

		ok_keys = ['name', 'address', 'facilities', 'openingTimes', 'reviews']

		# trim the keys:
		expected_data = [dict([(k, v) for k, v in loc_record.items() if k in ok_keys]) for loc_record in self.get_test_data()]
		

		# Set the ratings:
		if isinstance(ratings, dict):
			expected_data = [dict(**loc, rating=ratings[loc['name']]) for loc in expected_data]

		else:	
			expected_data = [dict(**loc, rating=ratings) for loc in expected_data]


		# Set the reviews:
		for loc in expected_data:
			loc['reviews'] = loc['reviews'][0:num_reviews]


		return expected_data


	def add_test_locations(self, add_reviews=False, clear_db=False):
		'''

		'''

		mongo_address = "mongodb://192.168.1.2:27017"
		mongo_client = MongoClient(mongo_address)

		if clear_db:
			mongo_client.drop_database('myLoc8r')


		# add data via the api:
		loc_api_url = self.build_url(path_parts=['api', 'locations'])

		for location in self.get_test_data():
			loc_post_r = requests.post(url=loc_api_url, json=location)

			self.assertEqual(loc_post_r.status_code, 201)


			if add_reviews:
				review_api_url = self.build_url(path_parts['api', 'locations', loc_post_r.json()['_id'], 'reviews'])

				for review in location['reviews']:
					review_post_r = requests.post(url=review_api_url, json=review)
					self.assertEqual(review_post_r.status_code, 201)


		# 2Mar2022: Have to reset the server connection to Mongo or the
		# $GeoNear seach will no work properly. I'm not sure why this happens
		# but resetting the connection is a workaround. 
		# reset_api_url = self.build_url(path_parts=['api', 'resetMongo'])
		# reset_r = requests.get(url=reset_api_url)
		# self.assertEqual(reset_r.status_code, 201)

		

		mongo_client['myLoc8r']['location'].create_index([('coords', pymongo.GEOSPHERE)])

		# part of resetting the connection:
		time.sleep(.5)




	def build_url(self, path_parts=[]):
		'''


		'''

		# complete url
		path = '/'.join(s.strip('/') for s in path_parts)
		url = urlunsplit((self.scheme, self.url, path, None, None))


		return url 

	def get_test_data(self):
		'''


		'''


		locations = [
			{        
				'name': 'Starcups',
				'address': "125 High Street, Reading, RG6 1PS",
				'facilities': "Hot drinks,Food,Premium wifi",
				'lng': -0.9690884,
				'lat': 51.455041,
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
				],
				'reviews': [
					{
						'author': "Simon Holmes",
						'rating': 5,
						'reviewText': "What a great place! I cannot say enough good things about it."
					},
					{
						'author': "Charlie Chaplin",
						'rating': 4,
						'reviewText': "It was okay. Coffee wasn't great, but the wifi was fast."
					},
				]
			},
			{        
				'name': 'Cafe Hero',
				'address': "555 High Street, Reading, RG6 1PS",
				'facilities': "Hot drinks,Premium wifi",
				'lng': -0.9690894,
				'lat': 51.455041,
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
				'reviews': [
					{
						'author': "Simon Holmes",
						'rating': 5,
						'reviewText': "What a great place! I cannot say enough good things about it."
					},
					{
						'author': "Charlie Chaplin",
						'rating': 1,
						'reviewText': "It was okay. Coffee wasn't great, but the wifi was fast."
					},
				]
			},
			{        
				'name': 'Burger Queen',
				'address': "783 High Street, Reading, RG6 1PS",
				'facilities': "Food,Premium wifi",
				'lng': -0.9690884,
				'lat': 51.455031,
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
					},
				],
				'reviews': [
					{
						'author': "Simon Holmes",
						'rating': 5,
						'reviewText': "No wifi. Has male and female a go-go dances. Will be back with the family!"
					},
					{
						'author': "Charlie Chaplin",
						'rating': 3,
						'reviewText': "Didn't get any work done, great place!"
					},
				]
			}

		]

		return locations

	def status_code_test(self, url, expected_status_code, test_status_code):
		'''


		'''

		err_msg = "{} returned a staus code of {}, expected status code: {}".format(url, test_status_code, expected_status_code)
		self.assertEqual(test_status_code, expected_status_code, msg=err_msg)




	def compare_data_objs(self, expected_data, test_data, err_msg_tag):
		'''
		
		Tests each value in two data dictionaries.

		if the value is a list then the length of the list is tested. But the
		items inside the list are not tested.

		# If a value is a list then it is tested to be empty.

		# If the list is not empty no tests are carried out.

		'''

		if (isinstance(expected_data, dict) and isinstance(test_data, dict)):

			# test both data sets are the same size:
			err_msg = "{} data sets do not have the same number of keys".format(err_msg_tag)
			self.assertEqual(len(test_data.keys()), len(expected_data.keys()), msg=err_msg)

			for k, v in expected_data.items():
				err_msg = "{}['{}']' do not match".format(err_msg_tag, k)

				if isinstance(v, list):
					self.assertEqual(len(test_data[k]), len(v), err_msg)


					# # check if list is empty, if empty then verify the test.k is empty
					# if len(v) == 0:
					# 	self.assertEqual(len(test_data[k]), len(v), err_msg)

					# else:
					# 	pass 

				else:
					# base case:
					self.assertEqual(test_data[k], v, msg=err_msg)

		else:
			err_msg = ''
			err_msg += "type(expected_data) = {}\n".format(type(expected_data))
			err_msg += "type(test_data) = {}\n".format(type(test_data))
			err_msg += "expected_data and test_data must both be of type dict()"
			err_msg += err_msg_tag
			raise ValueError(err_msg)


	def locations_page_test(self, expected_data, test_data):
		'''


		'''
		# test the lengths of the expected/test data. If the locations page is
		# empty test_data will be an empty list. And zip
		# (expected_data, test_data) will basically produce an empty list
		# thereby passing all tests which is not what we want.
		self.assertTrue(len(expected_data)>0, msg="No expected_data for testing")
		self.assertTrue(len(test_data)>0, msg="No test_data for testing. Possible cause of this failure is the scraper cannot find any data on the Locaitons page.")
		self.assertEqual(len(expected_data), len(test_data), msg='expected_data and test_data lengths do not match')
		
		# test the data in each location record matches the expected data:
		expected_data = sorted(expected_data, key=lambda x: x['name'])		
		test_data = sorted(test_data, key=lambda x: x['name'])

		for expected_loc, test_loc in zip(expected_data, test_data):

			error_msg_tag = "locations-list['{}']".format(expected_loc['name'])

			# print("expected_loc:\n{}\n".format(expected_loc))
			# print("test_loc:\n{}\n".format(test_loc))			

			self.compare_data_objs(
				expected_data=expected_loc,
				test_data=test_loc,
				err_msg_tag=error_msg_tag,
			)

	#  End Helper Methods:
	# *********************************************************************************




if __name__ == '__main__':
	unittest.main()


	# def compare_data_objs(self, expected_data, test_data, page_name, sub_doc_keys=list(), search_key=0, depth=0):
	# 	'''
		
	# 	Recursively tests data dictionaries.

	# 	If a list is encounted in expected_data then compare_data_objs() is
	# 	called again for each item in list with the matching item
	# 	in test_data. Matching is done with sub_doc_keys.

	# 	Ex: 

	# 	expected_data = [
	# 		{'name', 'item1', 'data1': '', 'data2': ''}
	# 		{'name', 'item2', 'data1': '', 'data2': ''}
	# 		{'name', 'item2', 'data1': '', 'data2': ''}

	# 	]

	# 	and 

	# 	test_data = [
	# 		{'name', 'item1', 'data1': 1, 'data2': ''}
	# 		{'name', 'item2', 'data1': 1, 'data2': ''}
	# 		{'name', 'item2', 'data1': 1, 'data2': ''}

	# 	]


	# 	then compare_data_objs() will be called again as follows:

	# 	compate_data_objs(
	# 		expected_data={'name', 'item1', 'data1': '', 'data2': ''},
	# 		test_data={'name', 'item1', 'data1': 1, 'data2': ''},
	# 		page_name=page_name.sub_docs_key,
	# 		sub_docs_key=sub_docs_key,
	# 		depth=(depth+1))

	# 	'''

	# 	if isinstance(expected_data, list):
	# 		# test each list item:

	# 		sub_doc_key = sub_doc_keys[search_key]
	# 		test_dict = dict([(data[sub_doc_key], data) for data in test_data])

	# 		for expected_record in expected_data:
	# 			test_record = test_dict[expected_record[sub_doc_key]]

	# 			# location-list['Star Cups']
	# 			# location-list['Star Cups']['reviews']
	# 			new_page_name = "{}['{}']".format(page_name, expected_record[sub_doc_key])

	# 			self.compare_data_objs(
	# 				expected_data=expected_record,
	# 				test_data=test_record,
	# 				page_name=new_page_name,
	# 				search_key=None,
	# 				sub_doc_keys=sub_doc_keys,
	# 				depth=(depth+1)
	# 			)


	# 	elif isinstance(expected_data, dict):
	# 		# test both data sets are the same size:
	# 		err_msg = "{} data sets do not have the same number of keys".format(page_name)
	# 		self.assertEqual(len(test_data.keys()), len(expected_data.keys()), msg=err_msg)

	# 		for k, v in expected_data.items():
	# 			err_msg = "{}.{} do not match".format(page_name, k)

	# 			if isinstance(v, list):
	# 				# recursive call:

	# 				# check if list is empty, if empty then verify the test.k is empty
	# 				if len(v) == 0:
	# 					self.assertEqual(len(test_data[k]), len(v), err_msg)

	# 				else:
	# 					base_page = expected_data[sub_doc_keys[0]]
	# 					new_page_name = "{}['{}']['{}']".format(page_name, base_page, k)

	# 					print(new_page_name)
						
	# 					print(page_name)
	# 					print(k)

	# 					raise ValueError("Recursive case, add tests")

	# 			else:
	# 				# base case:
	# 				self.assertEqual(test_data[k], v, msg=err_msg)

	# 	else:
	# 		err_msg = "No tests when type(expected_data) = {}".format(type(expected_data))
	# 		raise ValueError(err_msg)


