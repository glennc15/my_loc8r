import requests

from myloc8r_interface import myLoc8rInterface



class myLoc8rApiInterface(myLoc8rInterface):
	'''
	
	interacts with myLoc8r app through the api

	'''


	def __init__(self, url_builder_obj):
		'''


		'''

		self._url_builder_obj = url_builder_obj



	
	def register(self, name, email, password, profile_pic=None):
		'''

		profile_pic : conplete file path to the profile pic

		'''

		register_r = requests.post(
			url=self._url_builder_obj.url(['api', 'register']),
			json={
				'name': name,
				'email': email,
				'password': password
			}
		)


		if  register_r.status_code == 201:

			token = register_r.json()['token']
			
			# add a profile pic
			if profile_pic:
				profile_r = requests.post(
					url=self._url_builder_obj.url(['api', 'userprofile']),
					auth=(token, str(None)),
					files={'file': open(profile_pic, 'rb')}
				)

				if profile_r.status_code != 200:
					# this shoud probably be a warning???
					raise ValueError("problem adding a profile pic for user {}".format(email))


		else:
			raise ValueError("problem adding user {}".format(email))


		return token


	
	def login(self, email, password):
		'''

		'''

		login_r = requests.post(
			url=self._url_builder_obj.url(['api', 'login']),
			json={
				'email': email,
				'password': password
			}
		)


		if login_r.status_code == 200:
			token = login_r.json()['token']

		else:
			raise ValueError("Could not login user {}".format(email))



		return token 

	
	def add_location(self, name, address, facilities, longitude, latitude, operating_hours):
		'''

		'''
		pass


	
	def add_review(self, location, review, user):
		'''

		'''
		pass