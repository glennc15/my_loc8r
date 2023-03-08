

def locations_by_distance(request):
	locations_data = {}

	return (locations_data, 200)


def location_read(request, location_id):

	location_data = {
		'location_id': location_id
	}

	return (location_data, 200)


def location_update(request, location_id):

	location_data = {
		'location_id': location_id
	}

	return (location_data, 200)


def location_delete(request, location_id):

	location_data = {
		'location_id': location_id
	}

	return (location_data, 200)




