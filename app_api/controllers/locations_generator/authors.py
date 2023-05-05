


class Authors(object):
	'''
	
	Class for building authors for the myLoc8r app

	
	This generates an email address for each author and can hold 



	'''


	def __init__(self, data, myloc8r_interface):
		'''


		'''

		self._authors_dict = None 

		# build authors and log them in to myLoc8r app. This assumes the
		# authors hava already been added to the database.
		self.build_authors(data=data, myloc8r_interface=myloc8r_interface)




	@property
	def authors(self):
		return self._authors 

	@authors.setter
	def authors(self, value):
		self._authors = value




	# *******************************************************************************
	# START: helper methods:


	def build_authors(self, data, myloc8r_interface):
		'''


		'''

		author_objs = [Author(author) for author in data.authors]
		# login all authors/users:
		[author.login(myloc8r_interface) for author in author_objs]

		# make a dict where the key is the author name 

		self._authors_dict = dict([(x.name, x) for x in author_objs])

		self.authors = [x.name for x in author_objs]

		


	def get_author(self, author):
		'''

		'''

		return self._authors_dict[author]





	# END: helper methods:
	# *******************************************************************************



class Author(object):
	'''
	
	Class for an author/user in the myLoc8r app.

	Features:
	
	1) Generates an email and password for the author.
	2) can regiser/login to the myLoc8r app
	3) each author can write a location review to to the myLoc8r app


	'''

	def __init__(self, name, n=None):
		'''
		
		n: an integer to add to each email and password, n is required.

		'''

		if isinstance(name, tuple) or isinstance(name, list):
			self.name, n = name

		else:
			self.name = name 
		


		if n is None:
			raise ValueError("parameter n is required")


		self._email, self._password = self.get_email(n=n) 
		self.token = None

		# self._myloc8r_interface = myloc8r_interface 

		self._reviews = list()



	@property
	def name(self):
		return self._name 

	@name.setter
	def name(self, value):
		self._name = value


	@property
	def token(self):
		return self._token 

	@token.setter
	def token(self, value):
		self._token = value




	def login(self, myloc8r_interface):
		'''

		login a user on myLoc8r

		'''

		self.token = myloc8r_interface.login(
			email=self._email,
			password=self._password
		)




	def register(self, myloc8r_interface, profile_pic=None):
		'''

		add author to myLoc8r.

		can also upload a profile pic.

		profile_pic: full path to the profile pic 

		'''


		self._token = myloc8r_interface.register(
			name=self.name,
			email=self._email,
			password=self._password,
			profile_pic=profile_pic
		)







	def add_review(self, location_id, review):
		'''
		
		adds a review for the author to write. This does NOT add the review to
		myLoc8r.

		'''

		pass 



	def write_reviews(self):
		'''
		
		The author sends all reviews to myLoc8r app.

		'''

		pass 





	# *******************************************************************************
	# START: helper methods:	

	def get_email(self, n):
		'''
		
		generates an email and password:


		'''

		f_name, l_name = self.name.lower().split(' ')
		# removes any punctuation like O'Bannon 
		f_name = ''.join(e for e in f_name if e.isalpha())
		l_name = ''.join(e for e in l_name if e.isalpha())

		email = "{}{}{}@hotmail.com".format(f_name[0], l_name, n)
		password = "{}AbC123".format(n)


		return (email, password)



	# END: helper methods:	
	# *******************************************************************************



