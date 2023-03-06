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


