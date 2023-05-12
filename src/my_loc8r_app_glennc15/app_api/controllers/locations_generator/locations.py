import numpy as np 
import math 

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class Locations(object):
	'''

	Builds and stores Location object. Each location has random coordinates that are within a set distance from the origin


	'''


	def __init__(self, data, origin_longitude, origin_latitude, n=None, max_dist=2.5):
		'''

		n: the number of locations to generate. 

		'''	

		# self.names = list()

		self._locations = list()

		self.build_locations(data=data,
			origin_latitude=origin_latitude,
			origin_longitude=origin_longitude,
			max_dist=max_dist,
			n=n
		)



	@property
	def names(self):
		return self._names 

	@names.setter
	def names(self, value):
		self._names = value



	def locations(self):
		'''


		'''

		for location in self._locations:
			yield location 


	# def get_location(self, name):
	# 	'''


	# 	'''

	# 	return self._locations[name] 





	# *******************************************************************************
	# START: helper methods:


	def build_locations(self, data, origin_latitude, origin_longitude, max_dist, n):
		'''
		
		build location objects. Each location has coordinates that are a
		randon distacne and directection from the orign. Also each
		location has a random set of facilities.

		'''

		# check n is <= the number of shops:
		if (n is None) or (n > len(data.shops)):
			n = len(data.shops)




		locations = list()
		for shop in np.random.choice(a=data.shops, size=n, replace=False):
			name, address = shop.split('-')
			operating_hours = self.build_opening_records(record_strs=np.random.choice(data.operating_hours).split(','))
			latitude, longitude = self.random_coords(longitude_i=origin_longitude, latitude_i=origin_latitude, max_distance=max_dist)


			self._locations.append(Location(name=name, 
					address=address, 
					facilities=','.join(np.random.choice(data.shop_facilities, np.random.choice(range(1, 6)), replace=False)), 
					longitude=longitude, 
					latitude=latitude, 
					operating_hours=operating_hours, 
				)
			)


			# self.names.append(name)
			



	def random_coords(self, latitude_i, longitude_i, max_distance):
		'''

		'''
		rand_1, rand_2 = np.random.random_sample(2)

		distance = max_distance * rand_1
		bearing = 360 * rand_2

		latitude_f, longitude_f = self.getEndpoint(
			lat1=latitude_i, 
			lon1=longitude_i,
			bearing=bearing,
			d=distance
		)


		return (latitude_f, longitude_f)


	# random coordinates:
	def getEndpoint(self, lat1, lon1, bearing, d):
		'''
		

		giving and inital longitude/latitude, bearing and distance calculates
		the end point coordinates

		d: distance in km


		'''
		R = 6371                     #Radius of the Earth
		brng = math.radians(bearing) #convert degrees to radians
		#     d = d*1.852                  #convert nautical miles to km
		lat1 = math.radians(lat1)    #Current lat point converted to radians
		lon1 = math.radians(lon1)    #Current long point converted to radians
		lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))
		lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
		lat2 = math.degrees(lat2)
		lon2 = math.degrees(lon2)

		return (lat2, lon2)


	def convert_days(self, days):
		'''



		'''
		
		return days.replace('to', '-')


	def convert_time(self, time_str):
		'''



		'''


		return ''.join(time_str.lower().split(' '))
    
    
	def build_opening_time(self, opening_time_str):    
		'''



		'''

		days, times = opening_time_str.split(': ')
		opening, closing = times.split(' to ')
		
		opening_time_record = {
			'days': self.convert_days(days),
			'opening': self.convert_time(time_str=opening),
			'closing': self.convert_time(time_str=closing),
			'closed': False
		}

		
		return opening_time_record


	def build_opening_records(self, record_strs):
		'''



		'''

		isoweekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

		if len(record_strs) == 1:
			record_str = record_strs[0]
			this_opening_time = self.build_opening_time(opening_time_str=record_str)

			# add closed records as needed:
			start, end = this_opening_time['days'].split(' - ')
			isoweekday = isoweekdays.index(end)
			opening_times = [this_opening_time]

			for idx in range((isoweekday+1), 7):
				weekday = isoweekdays[(idx)]
				closed_time = {
				'days': isoweekdays[idx],
				'closed': True
				}

				opening_times.append(closed_time)

		else:
			opening_times = [self.build_opening_time(opening_time_str=x) for x in record_strs]


		return opening_times



	# END: helper methods:
	# *******************************************************************************








class Location(object):
	'''


	Class for a location for the myLoc8r app.


	Features:
	1) Stores a location instance.
	2) Can add it's location data to the database.



	'''

	def __init__(self, name, address, facilities, longitude, latitude, operating_hours):


		self._name = name 
		self._address = address
		self._facilities = facilities
		self._longitude = longitude
		self._latitude = latitude 
		self._operating_hours = operating_hours
		self.id = None


	@property
	def id(self):
		return self._id 

	@id.setter
	def id(self, value):
		self._id = value



	def add(self, myloc8r_interface):
		'''
		
		adds the location to the database

		'''

		self.id = myloc8r_interface.add_location(
			name=self._name, 
			address=self._address, 
			facilities=self._facilities, 
			longitude=self._longitude, 
			latitude=self._latitude, 
			operating_hours=self._operating_hours,
		)







