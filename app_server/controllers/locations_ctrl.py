from flask import render_template, url_for
# from bson import ObjectId

# import bson 

from urllib.parse import urlsplit, urlunsplit

import math

import requests

# import requests

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


def build_url(path, query=None, scheme=None, netloc=None):
	'''


	'''

	if scheme is None:
		scheme = 'http'

	if netloc is None:
		netloc = '127.0.0.1:5000'

	url = urlunsplit((scheme, netloc, path, query, None))


	return url 


def format_distance(distance):
	'''

	'''

	if isinstance(distance, float):
		if distance > 1:

			dist_formated = "{:.1f}km".format(distance)

		else:
			m_distance = int((distance*1000))
			dist_formated = "{:.0f}m".format(m_distance)

	else:
		dist_formated = '?'


	return dist_formated


def render_homepage(request, locations):
	'''


	'''
	
	message = None 

	if not isinstance(locations, list):
		message = 'API lookup error'
		locations = []

	else:
		if len(locations) == 0:
			message = "No places found nearby"



	locations_data = {
		'title': "myLoc8r - find a place to work with wifi",
		'page_header': {
			'title': 'myLoc8r',
			'strapline': 'Find places to work with wifi near you!'
		},
		'sidebar': "Looking for wifi and a seat? myLoc8r helps you find places to work when out and about. Perhaps with coffee, cake or a pint? Let Loc8r help you find the place you're looking for.",
		'locations': locations,
		'message': message
	}




	# 	[
	# 		{	
	# 			'_id': '6400f4cb08c1d613f894394a',
	# 			'name': 'Starcups',
	# 			'address': '125 High Street, Reading, RG6 1PS',
	# 			'rating': 3,
	# 			'facilities': ['Hot drinks', 'Food', 'Premium wifi'],
	# 			'distance': '100m'
	# 		}, 
	# 		{
	# 			'_id': '6400f4cb08c1d613f894394f',
	# 			'name': 'Cafe Hero',
	# 			'address': '125 High Street, Reading, RG6 1PS',
	# 			'rating': 4,
	# 			'facilities': ['Hot drinks', 'Food', 'Premium wifi'],
	# 			'distance': '200m'
	# 		}, 
	# 		{
	# 			'_id': '6400f4cb08c1d613f8943954',
	# 			'name': 'Burger Queen',
	# 			'address': '125 High Street, Reading, RG6 1PS',
	# 			'rating': 2,
	# 			'facilities': ['Food', 'Premium wifi'],
	# 			'distance': '250m'
	# 	}]

	# }

	return render_template('locations.html', **locations_data)





def locations_by_distance(request):
	'''


	'''

	api_url = url_for('api_locations', lng=-0.9690885, lat=51.455041, maxDistance=20)
	url_parts = urlsplit(api_url)
	api_url = build_url(
		path=url_parts.path,
		query=url_parts.query
	)

	# print('url = {}'.format(url))

	locations_r = requests.get(url=api_url)

	if locations_r.status_code == 200:
		locations = locations_r.json()

		for location in locations:
			location['distance'] = format_distance(distance=location['dist_calc'])
			location['facilities'] = location['facilities'].split(',')


	else:
		locaitons = []

	
	return render_homepage(request=request, locations=locations)

	
	# pdb.set_trace()

	# locations_data = {
	# 	'title': "myLoc8r - find a place to work with wifi",
	# 	'page_header': {
	# 		'title': 'myLoc8r',
	# 		'strapline': 'Find places to work with wifi near you!'
	# 	},
	# 	'sidebar': "Looking for wifi and a seat? myLoc8r helps you find places to work when out and about. Perhaps with coffee, cake or a pint? Let Loc8r help you find the place you're looking for.",
	# 	'locations': [
	# 		{	
	# 			'_id': '6400f4cb08c1d613f894394a',
	# 			'name': 'Starcups',
	# 			'address': '125 High Street, Reading, RG6 1PS',
	# 			'rating': 3,
	# 			'facilities': ['Hot drinks', 'Food', 'Premium wifi'],
	# 			'distance': '100m'
	# 		}, 
	# 		{
	# 			'_id': '6400f4cb08c1d613f894394f',
	# 			'name': 'Cafe Hero',
	# 			'address': '125 High Street, Reading, RG6 1PS',
	# 			'rating': 4,
	# 			'facilities': ['Hot drinks', 'Food', 'Premium wifi'],
	# 			'distance': '200m'
	# 		}, 
	# 		{
	# 			'_id': '6400f4cb08c1d613f8943954',
	# 			'name': 'Burger Queen',
	# 			'address': '125 High Street, Reading, RG6 1PS',
	# 			'rating': 2,
	# 			'facilities': ['Food', 'Premium wifi'],
	# 			'distance': '250m'
	# 	}]

	# }

	# return render_template('locations.html', **locations_data)



def render_details_page(location):
	'''


	'''
	location_data = {
		'title': location['name'],
		'page_header': {
			'title': location['name']
		},
		'sidebar': {
			'context': "is on myLoc8r because it has accessible wifi and space to sit down with your laptop and get some work done.",
			'callToAction': "If you've been and you like it - or if you don't - please leave a review to help other people just like you."
		},
		'location': location 
		}


		# {
		# 	'name': 'Starcups',
		# 	'address': '125 High Street, Reading, RG6 1PS',
		# 	'rating': 3,
		# 	'facilities': ['Hot drinks', 'Food', 'Premium wifi'],
		# 	'coords': {
		# 		'lat': 51.455041,
		# 		'lng': -0.9690884
		# 	},
		# 	'openingTimes': [
		# 		{
		# 			'days': 'Monday - Friday',
		# 			'opening': '7:00am',
		# 			'closing': '7:00pm',
		# 			'closed': False
		# 		}, 
		# 		{
		# 			'days': 'Saturday',
		# 			'opening': '8:00am',
		# 			'closing': '5:00pm',
		# 			'closed': False
		# 		}, 
		# 		{
		# 		'days': 'Sunday',
		# 		'closed': True
		# 		}
		# 	],
		# 	'reviews': [
		# 		{
		# 			'author': 'Simon Holmes',
		# 			'rating': 5,
		# 			'timestamp': '16 July 2013',
		# 			'reviewText': 'What a great place. I can\'t say enough good things about it.'
		# 		}, 
		# 		{
		# 			'author': 'Charlie Chaplin',
		# 			'rating': 3,
		# 			'timestamp': '16 June 2013',
		# 			'reviewText': 'It was okay. Coffee wasn\'t great, but the wifi was fast.'
		# 		}
		# 	]
		# }

	# }


	return render_template('location.html', **location_data)




def location(request, location_id):
	'''


	'''

	api_url = url_for('api_location', locationid=location_id)
	url_parts = urlsplit(api_url)
	api_url = build_url(
		path=url_parts.path,
		query=url_parts.query
	)

	# print('url = {}'.format(url))

	location_r = requests.get(url=api_url)

	# pdb.set_trace()

	if location_r.status_code == 200:
		location = location_r.json()
		# format the facilities as a list so it can render properly.
		location['facilities'] = location['facilities'].split(',')

		return render_details_page(location=location)



	else:
		# show error page:
		pass 




	# location_data = {
	# 	'title': 'Starcups',
	# 	'page_header': {
	# 		'title': 'Starcups'
	# 	},
	# 	'sidebar': {
	# 		'context': "is on myLoc8r because it has accessible wifi and space to sit down with your laptop and get some work done.",
	# 		'callToAction': "If you've been and you like it - or if you don't - please leave a review to help other people just like you."
	# 	},
	# 	'location': {
	# 		'name': 'Starcups',
	# 		'address': '125 High Street, Reading, RG6 1PS',
	# 		'rating': 3,
	# 		'facilities': ['Hot drinks', 'Food', 'Premium wifi'],
	# 		'coords': {
	# 			'lat': 51.455041,
	# 			'lng': -0.9690884
	# 		},
	# 		'openingTimes': [
	# 			{
	# 				'days': 'Monday - Friday',
	# 				'opening': '7:00am',
	# 				'closing': '7:00pm',
	# 				'closed': False
	# 			}, 
	# 			{
	# 				'days': 'Saturday',
	# 				'opening': '8:00am',
	# 				'closing': '5:00pm',
	# 				'closed': False
	# 			}, 
	# 			{
	# 			'days': 'Sunday',
	# 			'closed': True
	# 			}
	# 		],
	# 		'reviews': [
	# 			{
	# 				'author': 'Simon Holmes',
	# 				'rating': 5,
	# 				'timestamp': '16 July 2013',
	# 				'reviewText': 'What a great place. I can\'t say enough good things about it.'
	# 			}, 
	# 			{
	# 				'author': 'Charlie Chaplin',
	# 				'rating': 3,
	# 				'timestamp': '16 June 2013',
	# 				'reviewText': 'It was okay. Coffee wasn\'t great, but the wifi was fast.'
	# 			}
	# 		]
	# 	}

	# }

	# return render_template('location.html', **location_data)


