from urllib.parse import urlsplit
import bson
from bson import ObjectId
import re 
import json
import mongoengine as me


from my_loc8r.app_api.controllers.api_controllers_base import APIControllersBase
from my_loc8r.app_api.models.location_models import Locations, OpeningTime, Review

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class ReviewsAPIController(APIControllersBase):
	'''
	
	Controller class for review API routes.

	'''

	def __init__(self):
		'''

		'''

		super().__init__()


		self._required_review_keys = ['rating', 'reviewText']



# *******************************************************************************
# START: Public methods:
# 
# 




	# POST: /api/locations/<locationid>/reviews
	def create_review(self, location_id, review_data, user):
		'''
		
		author: user name from the authenticated user credentials.
 
		'''

		# sometimes review_data['reviewData'] exists, convert it to review_data['review_text']
		if review_data.get('reviewText'):
			review_data['review_text'] = review_data['reviewText']

		# remove any unnessary fields from review_data:
		review_data = dict([(k, v) for k, v in review_data.items() if k in ['rating', 'review_text']])

		# add author as the verified user name
		review_data['author'] = user.name
		review_data['author_id'] = user.id

		# Build a Review model using review_data and validate:
		review = Review(**review_data)

		try:
			review.validate()

		except Exception as e:
			if isinstance(e, me.errors.ValidationError):
				self.status_code = 400
				self.data = {'error': e.message}
				return None 

			else:
				raise e 


		# Get the location:
		try:
			location = Locations.objects(id=location_id).get()

		except Exception as e:
			if isinstance(e, me.errors.ValidationError):
				self.status_code = 404
				self.data = {'error': e.message}
				return None 

			elif isinstance(e, Locations.DoesNotExist):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			else:
				raise e 


		# add the review to the location:
		location.reviews.append(review)
		location.rating = self.get_location_rating(location_obj=location)

		try: 
			location.save()

		except Exception as e:
			print("500 Error!!!")
			raise e 


		# convert review._id to a string before sending the response:
		review_dict = review.to_mongo().to_dict()
		review_dict['_id'] = str(review_dict['_id'])
		review_dict['author_id'] = str(review_dict['author_id'])


		self.data = review_dict
		self.status_code = 201


	# GET: /api/locations/<locationid>/reviews/<reviewid>
	def read_review(self, location_id, review_id):
		'''

		# 26Mar23: using a '__raw__' query to match location_id and review_id

		# 12Mar23: I cannot come up with a query to return just a review that matches review_id.
		
		These queryies all return a Location:
		location = Location.objects(id=location_id).get()
		location = Location.objects(id=location_id, reviews__review_id=review).get()
		location = Location.objects(reviews__review_id=review).get()

		I've also tried .only('reviews') but still returns a Location.

		So finding the review in the location manually until I have more knowledge to build a better query.

		'''

		try:
			location = Locations.objects(__raw__={'_id': ObjectId(location_id), 'reviews._id': ObjectId(review_id)}).get()

		except Exception as e:
			if isinstance(e, me.errors.ValidationError):
				self.status_code = 404
				self.data = {'error': e.message}
				return None

			elif isinstance(e, Locations.DoesNotExist):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			elif isinstance(e, bson.errors.InvalidId):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			else:
				raise e 


		# get the right review:
		target_review = [x for x in location.reviews if x._id == ObjectId(review_id)][0].to_mongo().to_dict()
		target_review['_id'] = str(target_review['_id'])
		target_review['author_id'] = str(target_review['author_id'])


		self.status_code = 200
		self.data = target_review


	# PUT: /api/locations/<locationid>/reviews/<reviewid>
	def update_review(self, location_id, review_id, review_data, user):
		'''


		'''


		# Validate the review_data. Locations.objects().update() will write
		# invalid review data to the db for a subdocument. It will throw an
		# error is a locaiton.save() operation is performed but the invalid
		# data is still written to the db.

		if not self.is_review_data_ok(review_data=review_data):
			return None 

		# convert 'reviewText' to 'review_text" if necessary and remove any
		# unneeded fields.
		if review_data.get('reviewText'):
			review_data['review_text'] = review_data['reviewText']

		# remove any unnessary fields from review_data:
		review_data = dict([(k, v) for k, v in review_data.items() if k in ['rating', 'review_text']])


		# add author as the verified user name and id. The update only
		# uses .rating and .review_text but the validation requires .author
		# and .author_id

		review_data['author'] = user.name
		review_data['author_id'] = user.id

		review = Review(**review_data)

		# pdb.set_trace()

		try:
			review.validate()

		except Exception as e:
			if isinstance(e, me.errors.ValidationError):
				self.status_code = 400
				self.data = {'error': e.message}
				return None 

			else:
				raise e 




		# Build the seach query:

		# is locaiton_id or review_id is not a valid bson string an error will be thrown:
		try:
			search_query = {
				'_id': ObjectId(location_id),
				'reviews': {
					"$elemMatch": {
						'_id': ObjectId(review_id),
						'author_id': user.id
					}
				}
			}


		except Exception as e:
			# if isinstance(e, me.errors.ValidationError):
			# 	self.status_code = 404
			# 	self.data = {'error': e.message}
			# 	return None

			# elif isinstance(e, Locations.DoesNotExist):
			# 	self.status_code = 404
			# 	self.data = {'error': str(e)}
			# 	return None

			if isinstance(e, bson.errors.InvalidId):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			else:
				raise e 


		# Build the set query. This is what updates the review:
		set_query = {
			'$set': {
				'reviews.$.rating': review_data['rating'], 
				'reviews.$.review_text': review_data['review_text'], 

			}
		}


		# print("search_query = {}".format(search_query))
		# pdb.set_trace()

		# pdb.set_trace()

		try:
			location = Locations.objects(__raw__=search_query).update(__raw__=set_query)


		except Exception as e:
			if isinstance(e, me.errors.ValidationError):
				self.status_code = 404
				self.data = {'error': e.message}
				return None

			elif isinstance(e, Locations.DoesNotExist):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			elif isinstance(e, bson.errors.InvalidId):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			else:
				raise e 


		# on a successful update location is an interger = 1. The location
		# rating needs to be updated after updating the review.
		if location == 1:
			location = Locations.objects(id=location_id).get()
			location.rating = self.get_location_rating(location_obj=location)
			location.save()

			self.read_review(location_id=location_id, review_id=review_id)


		elif location == 0:

			# Search for the location again without the author. If the
			# locaiton can be found and the author does match then it's a 404 error.

			try:
				location = Locations.objects(__raw__={'_id': ObjectId(location_id), 'reviews._id': ObjectId(review_id)}).get()

			except Exception as e:
				if isinstance(e, me.errors.ValidationError):
					self.status_code = 404
					self.data = {'error': e.message}
					return None

				elif isinstance(e, Locations.DoesNotExist):
					self.status_code = 404
					self.data = {'error': str(e)}
					return None

				elif isinstance(e, bson.errors.InvalidId):
					self.status_code = 404
					self.data = {'error': str(e)}
					return None

				else:
					raise e


			# get the target review and check if the authors match:
			target_review = [x for x in location.reviews if x._id == ObjectId(review_id)][0]


			if target_review.author_id != user.id:
					self.status_code = 403
					self.data = {'error': "User with id {} cannot update this review with id {}".format(user.id, target_review._id)}
					return None

			else:
				raise ValueError("Error during update review!")



		else:
			raise ValueError("location = {}".format(location))



	# DELETE: /api/locations/<locationid>/reviews/<reviewid>
	def delete_review(self, location_id, review_id, user):
		'''


		'''

		# if review_id is invalid then ObjectId(review_id) will throw and error:
		try:
			raw_query = {
				"$pull": {
					"reviews": {'_id': ObjectId(review_id)}
				}
			}

		except Exception as e:
			if isinstance(e, bson.errors.InvalidId):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None


		# Build the seach query:

		# is locaiton_id or review_id is not a valid bson string an error will be thrown:
		try:
			search_query = {
				'_id': ObjectId(location_id),
				'reviews': {
					"$elemMatch": {
						'_id': ObjectId(review_id),
						'author_id': user.id
					}
				}
			}


		except Exception as e:
			# if isinstance(e, me.errors.ValidationError):
			# 	self.status_code = 404
			# 	self.data = {'error': e.message}
			# 	return None

			# elif isinstance(e, Locations.DoesNotExist):
			# 	self.status_code = 404
			# 	self.data = {'error': str(e)}
			# 	return None

			if isinstance(e, bson.errors.InvalidId):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			else:
				raise e 

		# pdb.set_trace()

		try:
			location = Locations.objects(__raw__=search_query).update(__raw__=raw_query)

		except Exception as e:
			if isinstance(e, me.errors.ValidationError):
				self.status_code = 404
				self.data = {'error': e.message}
				return None

			elif isinstance(e, Location.DoesNotExist):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			elif isinstance(e, bson.errors.InvalidId):
				self.status_code = 404
				self.data = {'error': str(e)}
				return None

			else:
				raise e 


		# on a successful delete location is an interger = 1:
		if location == 1:
			# update the location rating:
			location = Locations.objects(id=location_id).get()
			location.rating = self.get_location_rating(location_obj=location)
			location.save()

			self.data = {'message': "deleted review with id = {}".format(review_id)}
			self.status_code = 204

		elif location == 0:
			# Search for the location again without the author. If the
			# locaiton can be found and the author does match then it's a 404 error.

			try:
				location = Locations.objects(__raw__={'_id': ObjectId(location_id), 'reviews._id': ObjectId(review_id)}).get()

			except Exception as e:
				if isinstance(e, me.errors.ValidationError):
					self.status_code = 404
					self.data = {'error': e.message}
					return None

				elif isinstance(e, Locations.DoesNotExist):
					self.status_code = 404
					self.data = {'error': str(e)}
					return None

				elif isinstance(e, bson.errors.InvalidId):
					self.status_code = 404
					self.data = {'error': str(e)}
					return None

				else:
					raise e


			# get the target review and check if the authors match:
			target_review = [x for x in location.reviews if x._id == ObjectId(review_id)][0]


			if target_review.author_id != user.id:
					self.status_code = 403
					self.data = {'error': "User with id {} cannot delete this review with id {}".format(user.id, target_review._id)}
					return None

			else:
				raise ValueError("Error during update review!")


		# # happens with the location and/or the review do not exists:
		# elif location == 0:
		# 	self.status_code = 404
		# 	self.data = {'error': 'No location with an id = {} and/or a review with and id = {}'.format(location_id,  review_id)}
		# 	return None

		else:
			raise ValueError("unknow error, location = {}".format(location))


	# End: Public methods:
	# *******************************************************************************


	# *******************************************************************************
	# START: helper methods:


	def is_review_data_ok(self, review_data):

		'''
		 
		checks review_data contains the required fields:

		'''

		review_data_ok = True
		error_dict = dict()

		# check all required keys are in review_data:
		for required_key in self._required_review_keys:
			if required_key not in review_data.keys():
				error_dict[required_key] = "{} field is required".format(required_key)
				review_data_ok = False


		if review_data_ok == False:
			self.status_code = 400
			self.data = error_dict


		return review_data_ok

		# review = Review(
		# 	author=review_data['author'],
		# 	rating=review_data['rating'],
		# 	review_text=review_data['reviewText']
		# )

		# validate each field in review_data using the  



	# End: helper methods:
	# *******************************************************************************




