from flask import render_template
# from bson import ObjectId

def locations_by_distance(request):
	'''


	'''

	locations_data = {
		'title': "myLoc8r - find a place to work with wifi",
		'page_header': {
			'title': 'myLoc8r',
			'strapline': 'Find places to work with wifi near you!'
		},
		'sidebar': "Looking for wifi and a seat? myLoc8r helps you find places to work when out and about. Perhaps with coffee, cake or a pint? Let Loc8r help you find the place you're looking for.",
		'locations': [
			{	
				'_id': '6400f4cb08c1d613f894394a',
				'name': 'Starcups',
				'address': '125 High Street, Reading, RG6 1PS',
				'rating': 3,
				'facilities': ['Hot drinks', 'Food', 'Premium wifi'],
				'distance': '100m'
			}, 
			{
				'_id': '6400f4cb08c1d613f894394f',
				'name': 'Cafe Hero',
				'address': '125 High Street, Reading, RG6 1PS',
				'rating': 4,
				'facilities': ['Hot drinks', 'Food', 'Premium wifi'],
				'distance': '200m'
			}, 
			{
				'_id': '6400f4cb08c1d613f8943954',
				'name': 'Burger Queen',
				'address': '125 High Street, Reading, RG6 1PS',
				'rating': 2,
				'facilities': ['Food', 'Premium wifi'],
				'distance': '250m'
		}]

	}

	return render_template('locations.html', **locations_data)


def location(request):
	'''


	'''

	location_data = {
		'title': 'Starcups',
		'page_header': {
			'title': 'Starcups'
		},
		'sidebar': {
			'context': "is on myLoc8r because it has accessible wifi and space to sit down with your laptop and get some work done.",
			'callToAction': "If you've been and you like it - or if you don't - please leave a review to help other people just like you."
		},
		'location': {
			'name': 'Starcups',
			'address': '125 High Street, Reading, RG6 1PS',
			'rating': 3,
			'facilities': ['Hot drinks', 'Food', 'Premium wifi'],
			'coords': {
				'lat': 51.455041,
				'lng': -0.9690884
			},
			'openingTimes': [
				{
					'days': 'Monday - Friday',
					'opening': '7:00am',
					'closing': '7:00pm',
					'closed': False
				}, 
				{
					'days': 'Saturday',
					'opening': '8:00am',
					'closing': '5:00pm',
					'closed': False
				}, 
				{
				'days': 'Sunday',
				'closed': True
				}
			],
			'reviews': [
				{
					'author': 'Simon Holmes',
					'rating': 5,
					'timestamp': '16 July 2013',
					'reviewText': 'What a great place. I can\'t say enough good things about it.'
				}, 
				{
					'author': 'Charlie Chaplin',
					'rating': 3,
					'timestamp': '16 June 2013',
					'reviewText': 'It was okay. Coffee wasn\'t great, but the wifi was fast.'
				}
			]
		}

	}

	return render_template('location.html', **location_data)


