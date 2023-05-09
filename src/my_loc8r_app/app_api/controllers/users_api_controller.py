import datetime
import mongoengine as me
import re 

from my_loc8r_app.app_api.controllers.api_controllers_base import APIControllersBase
from my_loc8r_app.app_api.models.user_model import Users

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class UsersAPIController(APIControllersBase):
	'''
	
	Controller class for User API routes.

	'''

	def __init__(self):
		'''

		'''

		super().__init__()

		self._required_registration_keys = ['name', 'email', 'password']
		self._required_login_keys = ['email', 'password']



# *******************************************************************************
# START: Public methods:

	# POST: /api/register
	def register(self, registration_data):
		'''


		'''

		# registration_data = request.json

		# if self.is_user_data_ok(registration_data=registration_data, required_keys=self._required_registration_keys):
		if self.is_user_ok(registration_data=registration_data, required_keys=self._required_registration_keys):

			user = Users(
				name=registration_data['name'],
				email=registration_data['email'],
			)

			user.hash_password(password=registration_data['password'])

			try:
				user.save()

			except Exception as e:
				# raise e 
				if isinstance(e, me.errors.NotUniqueError):
					self.status_code = 400
					self.data = {"error": "A user for {} already exists".format(registration_data['email'])}

					return None 

				else:
					raise e 


			self.status_code = 201
			self.data = {'token': user.generate_jwt()}



	# POST: /api/login
	def login(self, login_data):
		'''


		'''


		# login_data = request.json 

		if self.is_user_ok(registration_data=login_data, required_keys=self._required_login_keys):

			try:
				user = Users.objects(email=login_data['email']).get()

			except Exception as e:
				# raise e
				if isinstance(e, me.errors.DoesNotExist):
					self.status_code = 400
					self.data = {"error": "No user for email {}".format(login_data['email'])}

					return None 

				else:
					raise e 


			# verify password:
			if user.verify_password(password=login_data['password']):
				self.status_code = 200
				self.data = {'token': user.generate_jwt()}


			else:
				self.status_code = 401
				self.data = {'error': "password for {} is incorrect.".format(login_data['email'])}



	# End: Public methods:
	# *******************************************************************************			


	def is_user_ok(self, registration_data, required_keys):
		'''


		'''

		registration_data_ok = True

		error_dict = dict()


		# check all required keys are in registartion data:
		for required_key in required_keys:
			if required_key not in registration_data.keys():
				error_dict[required_key] = "{} field is required".format(required_key)
				registration_data_ok = False

		# validate each value and check for empty strings:
		for key, value in registration_data.items():

			user = Users()

			if (key in required_keys) and (key!='password'):



				# remove all leading and trailing spaces from strings:
				if isinstance(value, str):
					user[key] = value.strip()

				else:
					user[key] = value

				try:
					user.validate()

				except Exception as e:

					if isinstance(e, me.errors.ValidationError):
						error_dict[key] = "a value of '{}' is not valid for field {}".format(value, key)
						registration_data_ok = False						

					else:
						print("e = {}".format(e))
						print("type(e) = {}".format(type(e)))
						raise e 


			elif (key in required_keys) and (key=='password'):
				if not user.validate_password(password=value):
					error_dict[key] = "a value of '{}' is not valid for field {}".format(value, key)
					registration_data_ok = False	



		if registration_data_ok == False:
			self.status_code = 400
			self.data = error_dict


		return registration_data_ok





































