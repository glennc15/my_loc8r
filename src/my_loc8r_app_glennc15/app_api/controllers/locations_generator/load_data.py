import os 
import json 



class LoadData(object):
	'''
	
	Convience class to load the 'cafe_data.json' file.  Has attributes for:

	.authors 
	.shops
	.positive_reviews
	.negative_reviews
	.moderate_reviews
	.shop_facilties
	.operating_hours

	'''


	def __init__(self):
		'''


		'''
	
		self.load_data_file()



	@property
	def authors(self):
		return self._authors 

	@authors.setter
	def authors(self, value):
		self._authors = value


	@property
	def shops(self):
		return self._shops 

	@shops.setter
	def shops(self, value):
		self._shops = value


	@property
	def positive_reviews(self):
		return self._positive_reviews 

	@positive_reviews.setter
	def positive_reviews(self, value):
		self._positive_reviews = value


	@property
	def negative_reviews(self):
		return self._negative_reviews 

	@negative_reviews.setter
	def negative_reviews(self, value):
		self._negative_reviews = value

	@property
	def moderate_reviews(self):
		return self._moderate_reviews 

	@moderate_reviews.setter
	def moderate_reviews(self, value):
		self._moderate_reviews = value


	@property
	def shop_facilities(self):
		return self._shop_facilities 

	@shop_facilities.setter
	def shop_facilities(self, value):
		self._shop_facilities = value


	@property
	def operating_hours(self):
		return self._operating_hours 

	@operating_hours.setter
	def operating_hours(self, value):
		self._operating_hours = value




	# *******************************************************************************
	# START: helper methods:	

	def load_data_file(self):
		'''


		'''


		# /Users/glenn/Documents/GettingMEAN/my_loc8r/app_api/controllers/locations_generator
		# data_file = open(os.path.join(os.getcwd(), 'cafe_data.json'), 'r')

		filepath = os.path.join(os.getcwd(), 'app_api/controllers/locations_generator/cafe_data.json')


		if not os.path.exists(filepath):
			filepath = os.path.join(os.getcwd(), 'cafe_data.json')


		data_file = open(filepath, 'r')

		data = json.loads(data_file.read())
		data_file.close()

		self.authors = data['authors']
		self.positive_reviews = data['reviews_positive']
		self.moderate_reviews = data['reviews_moderate']
		self.negative_reviews = data['reviews_negative']
		self.shop_facilities = data['facilities']
		self.operating_hours = data['operating_hours']
		self.shops = data['shops']







	# END: helper methods:	
	# *******************************************************************************
