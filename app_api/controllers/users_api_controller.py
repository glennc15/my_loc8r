
from my_loc8r.app_api.models.user_model import User


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


		if self.is_registration_data_ok(registration_data=request.json):
			pass 






	def login(self, request):
		'''


		'''


		pass 




	def is_registration_data_ok(self, registration_data):
		'''


		'''

		registration_data_ok = True

		error_dict = dict()

		user = User()


		# check all required keys are in registartion data:
		for required_key in self._required_registration_keys:
			if required_key not in registration_data.keys():
				error_dict[required_key] = "{} field is required".format(required_key)
				registration_data_ok = False

		# validate each value and check for empty strings:
		for key, value in registration_data.items():
			
			# empty string:
			if isinstance(value, str) and (len(value)==0):
				error_dict[key] = "a value of '{}' is not valid for field {}".format(registration_data[key], key)
				registration_data_ok = False


			# validations for password:
			elif key == 'password':
				pass

			# validations for remaining keys:
			else:
				user = User()
				user[key] = registration_data[key]

				try:
					user.validate()

				except Exception as e:
					error_dict[key] = "a value of '{}' is not valid for field {}".format(registration_data[key], key)
					registration_data_ok = False





		if registration_data_ok == False:
			self.status_code = 400
			self.data = error_dict



		# pdb.set_trace()




		return registration_data_ok





































