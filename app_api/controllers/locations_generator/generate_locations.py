import os 
import numpy as np 
import datetime 

from my_loc8r.app_api.controllers.locations_generator.load_data import LoadData
from my_loc8r.app_api.controllers.locations_generator.locations import Locations
from my_loc8r.app_api.controllers.locations_generator.authors import Authors

from my_loc8r.app_api.controllers.locations_generator.myloc8r_ctrl_interface import myLoc8rCtrlInterface



import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class GenerateLocations(object):
	'''
	
	Generates Locations with reviews and adds them to the database.

	'''

	def __init__(self, origin_longitude, origin_latitude, max_dist, n, existing_locations, location_ctrl_obj):
		'''


		'''

		data = self.get_data(existing_locations=existing_locations)

		self._locations = Locations(
			origin_latitude=origin_latitude,
			origin_longitude=origin_longitude,
			max_dist=max_dist,
			n=n,
			data=data 
		) 

		myLoc8rInterface = myLoc8rCtrlInterface(locations_ctrl_obj=location_ctrl_obj)

		# add the locations to the database and login all users:
		[x.add(myLoc8rInterface) for x in self._locations.locations()]

		self._users = Authors(data=data, myloc8r_interface=myLoc8rInterface)


		# add reviews for each location:
		for location in self._locations.locations():
			for review_record in self.get_reviews(data=data):
				# reading location for each review. This updates the location
				# viewd counter
				myLoc8rInterface.read_location(location_id=location.id)

				# add the review to the location:
				myLoc8rInterface.add_review(
					location=location,
					review=review_record,
					user=self._users.get_author(author=review_record['author'])
				)


	# *******************************************************************************
	# START: Public methods:








	# END: Public methods:
	# *******************************************************************************




	# *******************************************************************************
	# START: Helper methods:


	def add_reviews(self, data):
		'''


		'''

		pass 


	def get_reviews(self, data):
		'''
		
		generates a list of reviews.

		all attributes of the review are random includeing the author, review
		rating, and review text.
		

		There are 3 categories of reviews (positive, negative, moderate). Each
		random review rating is used to select a proper review text from
		each review category.

		'''

		# rating is scaled to 6 to start with and then scaled between 1 and 5.
		max_rating = 6 

		# the number of reviews is random.  
		number_of_reviews, rating = np.random.random_sample(2)

		# scale number_of_reviews, minimum is 3 reviews
		number_of_reviews = int(number_of_reviews*len(data.positive_reviews))

		if number_of_reviews < 3:
			number_of_reviews = 3


		# scale ratings. make samples from the normal disturbution with mean
		# of rating. Trying to get all review ratings to roughly average to
		# rating.
		rating = rating * max_rating

		# these are ratings for each review:
		ratings = np.random.normal(loc=rating, scale=1.25, size=number_of_reviews)


		# now count the number of positive reviews, moderate reviews, and
		# negative reviews. These counts will be used to make random samples
		# from each catagory of reviews:
		positive_reviews = 0
		moderate_reviews = 0
		negative_reviews = 0

		for this_rating in ratings:
			if this_rating <2:
				negative_reviews += 1

			elif 2 <= this_rating < 4:
				moderate_reviews += 1

			else:
				positive_reviews += 1


		# select the correct number of each reviews:
		positive_reviews = np.random.choice(a=data.positive_reviews, size=positive_reviews, replace=False).tolist()
		moderate_reviews = np.random.choice(a=data.moderate_reviews, size=moderate_reviews, replace=False).tolist()
		negative_reviews = np.random.choice(a=data.negative_reviews, size=negative_reviews, replace=False).tolist()

		# authors for each review:
		these_authors = np.random.choice(a=self._users.authors, size=number_of_reviews, replace=False)
		review_records = list()

		# Finally: can build each review record:

		for this_rating, author in zip(ratings, these_authors):

			if this_rating < 2:
				this_review = negative_reviews.pop()

			elif 2 <= this_rating < 4:
				this_review = moderate_reviews.pop()

			else:
				this_review = positive_reviews.pop()


			# convert rating to an int 1 <= rating <= 5:
			this_rating = int(this_rating)

			if this_rating < 1:
				this_rating = 1 

			elif this_rating > 5:
				this_rating = 5 

			review_records.append({
				'author': author,
				'rating': this_rating,
				'reviewText': this_review,
				'created_on': None 
			})


		self.add_review_dates(review_records=review_records)


		return review_records


	def add_review_dates(self, review_records):
		'''
		
		fills in the created_on attribute for each review record.

		Each shop is assumed to be open for 1 year. So each review will get a
		randomly generated time between 1 year and the curren time.


		'''

		time_deltas = np.random.random_sample(len(review_records)) * 365

		start_timestamp = datetime.datetime.utcnow() - datetime.timedelta(days=365)

		for review_record, time_delta in zip(review_records, time_deltas):
			review_record['created_on'] = start_timestamp + datetime.timedelta(days=time_delta)




	def get_data(self, existing_locations):
		'''


		'''

		# remove existing shops:
		data = LoadData()
		data.shops = [x for x in data.shops if (x.split('-')[0]).strip() not in existing_locations]


		return data 


	# END: Helper methods:
	# *******************************************************************************