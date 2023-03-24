import datetime
import mongoengine as me

from my_loc8r.app_api.models.user_model import Users

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class UsersAPIController(object):
	'''
	
	Controller class for User API routes.

	'''

	def __init__(self):
		'''

		'''

		self.status_code = None 
		self.data = None

		self._required_registration_keys = ['name', 'email', 'password']
		self._required_login_keys = ['email', 'password']


# *******************************************************************************
# START: Public methods:


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


	def register(self, request):
		'''


		'''

		registration_data = request.json

		if self.is_user_data_ok(registration_data=registration_data, required_keys=self._required_registration_keys):

			user = Users(
				name=registration_data['name'],
				email=registration_data['email'],
			)

			user.set_password(password=registration_data['password'])

			try:
				user.save()

			except Exception as e:

				if isinstance(e, me.errors.NotUniqueError):
					self.status_code = 400
					self.data = {"error": "A user for {} already exists".format(registration_data['email'])}

					return None 

				else:
					raise e 


			self.status_code = 201
			self.data = {'token': user.generate_jwt()}




	def login(self, request):
		'''


		'''


		pass 




	def is_user_data_ok(self, registration_data, required_keys):
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
			
			# empty string:
			if isinstance(value, str) and (len(value.strip())==0):
				error_dict[key] = "a value of '{}' is not valid for field {}".format(value, key)
				registration_data_ok = False


			# validations for password:
			elif key == 'password':
				pass

			# validations for remaining keys:
			else:
				user = Users()

				if isinstance(value, str):
					user[key] = value.strip()

				else:
					user[key] = value

				try:
					user.validate()

				except Exception as e:
					error_dict[key] = "a value of '{}' is not valid for field {}".format(value, key)
					registration_data_ok = False


		if registration_data_ok == False:
			self.status_code = 400
			self.data = error_dict


		return registration_data_ok





































