from abc import ABC, abstractmethod


class myLoc8rInterface(ABC):
	'''
	
	Interface for interacting the myLoc8r app.  


	'''


	@abstractmethod
	def register(self, name, email, password, profile_pic=None):
		raise NotImplementedError


	@abstractmethod
	def login(self, email, password):
		raise NotImplementedError


	@abstractmethod
	def add_location(self, name, address, facilities, longitude, latitude, operating_hours):
		raise NotImplementedError


	@abstractmethod
	def add_review(self, location, review, user):
		raise NotImplementedError