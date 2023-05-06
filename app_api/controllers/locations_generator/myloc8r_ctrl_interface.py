import requests

from my_loc8r.app_api.controllers.locations_generator.myloc8r_interface import myLoc8rInterface
from my_loc8r.app_api.controllers.users_api_controller import UsersAPIController
from my_loc8r.app_api.controllers.reviews_api_controller import ReviewsAPIController
from my_loc8r.app_api.models.user_model import Users



# from my_loc8r.app_api.controllers.locations_api_controller import LocationsAPIController


import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class myLoc8rCtrlInterface(myLoc8rInterface):
	'''
	
	interacts with myLoc8r app through the api controller objects. 


	'''


	def __init__(self, locations_ctrl_obj):
		'''


		'''

		self._locations_ctrl_obj = locations_ctrl_obj



	
	def register(self, name, email, password, profile_pic=None):
		'''

		profile_pic : conplete file path to the profile pic

		'''

		user_ctrl = UsersAPIController()

		user_ctrl.register(registration_data={
			'name': name,
			'email': email,
			'password': password
		})


		if user_ctrl.status_code != 201:
			raise ValueError("Problem registering user {}".format(email))


		return user_ctrl.data['token'] 


	
	def login(self, email, password):
		'''

		'''

		user_ctrl = UsersAPIController()

		user_ctrl.login(login_data={
			'email': email,
			'password': password
		})


		if user_ctrl.status_code != 200:
			raise ValueError("Problem logging in user {}".format(email))


		return user_ctrl.data['token'] 

	
	def add_location(self, name, address, facilities, longitude, latitude, operating_hours):
		'''

		'''
		# location_ctrl = LocationsAPIController()locations_ctrl_obj


		location_ctrl = self._locations_ctrl_obj

		location_ctrl.create_location(location_data={
			'name': name,
			'address': address,
			'facilities': facilities,
			'openingTimes': operating_hours,
			'lng': longitude,
			'lat': latitude
		})


		if location_ctrl.status_code != 201:
			raise ValueError('Problem adding location {} to the databaser'.format(name))


		# return the locations id:
		return location_ctrl.data['_id']



	
	def add_review(self, location, review, user):
		'''

		'''

		
		user, error_msg = Users.verify_jwt(jwt_token=user.token)


		review_ctrl = ReviewsAPIController()

		review_ctrl.create_review(
			location_id=location.id,
			review_data=review,
			user=user 
		)


		if review_ctrl.status_code != 201:
			raise ValueError('Problem adding a review to location = {} to the databaser'.format(location.id))


	def read_location(self, location_id):
		'''
		

		
		'''

		self._locations_ctrl_obj.read_location_by_id(location_id=location_id)


		if self._locations_ctrl_obj.status_code != 200:
			raise ValueError('Problem reading location = {} to the databaser'.format(location_id))









