import json
from bson import ObjectId


from my_loc8r.app_api.models.location_models import Location, OpeningTime, Review

# def convert_object_ids(document):
# 	pass 


import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


def build_opening_times(opening_times_list):
	'''


	'''

	# add the opening time sub documents:
	opening_time_records = list()
	for opening_time in opening_times_list:
		# print("opening_time= {}".format(opening_time))

		# check required data days and closed:
		if not opening_time.get('days'):
			# print("Error opeing_time['days']")
			response = ({'message': "{}.opening_times is invalide. Missing days.".format(location['name'])}, 400)
			break
		
		elif (not opening_time.get('closed') and (opening_time['closed']!=False)):
			# print("Error opeing_time['closed']")
			response = ({'message': "{}.opening_times is invalide. Missing data".format(location['name'])}, 400)
			break
		
		else:
			# add valid opening time:
			if opening_time['closed']:
				opening_record = OpeningTime(
					days=opening_time['days'],
					closed=opening_time['closed']
				)

			else:
				opening_record = OpeningTime(
					days=opening_time['days'],
					opening=opening_time['opening'],
					closing=opening_time['closing'],
					closed=False 
					)

			opening_time_records.append(opening_record)


	return opening_time_records



def convert_object_ids(document):
	'''
	
	Mongo ObjectId cannot be converted to JSON.

	Each Mongoengine Document class has a .to_json() method but it converts
	ObjectIds to {'$oid': '6408a9dcdec8287c6dfd03d6'}
	
	So converts all ObjectId objects to strings

	'''

	record = json.loads(document.to_json())

	# # convert the ObjectId in the location object:
	record['_id'] = record['_id']['$oid']

	# convert the ObjectId for each opeing time sub document
	for opening_time in record['openingTimes']:
		opening_time['_id'] = opening_time['_id']['$oid']

	# convert the ObjectId for each review sub document
	for review in record['reviews']:
		review['_id'] = review['_id']['$oid']


	return record 


def locations_by_distance(request):
	locations_data = {}

	return (locations_data, 200)


def location_create(request):

	location_data = request.get_json()

	# check required location data:
	if not location_data.get('name'):
		response = ({'message': "name is required"}, 400)

	elif len(location_data.get('name')) == 0:
		response = ({'message': "name='{}'is not valid".format(location_data['name'])}, 400)

	elif not location_data.get('lng'):
		response = ({'message': "longitude (lng) is required"}, 400)

	elif not location_data.get('lat'):
		response = ({'message': "latitue (lat) is required"}, 400)

	else:
		# location data is ok so build a location:
		location = Location(
			name=location_data['name'],
			address=location_data['address'],
			facilities=location_data['facilities'],
			coords = [location_data['lng'], location_data['lat']]
		)

		opening_time_records = build_opening_times(opening_times_list=location_data['openingTimes'])
		location.openingTimes = opening_time_records

		try:
			location.save()

			# remove the ObjectId objects:
			location_data = convert_object_ids(document=location)

			response = (location_data, 201)

		except Exception as e:
			print("500 Error!")
			print(e)
			response = (e, 500)


	return response



def location_read(request, locationid=None):


	if locationid is None:
		response = ({"message": "locationid is required"}, 404)

	else:

		try:

			location = Location.objects(id=locationid).get()
			# remove the object ids:
			location_data = convert_object_ids(document=location)

			response = (location_data, 200)

		except Exception as e:

			err_msg = "{} is not a valid id for a locaiton.".format(locationid)
			# err_msg += e

			response = (err_msg, 404)


	return response 


def location_update(request, locationid=None):

	if locationid is None:
		response = ({"message": "locationid is required"}, 404)

	else:

		try:
			location = Location.objects(id=locationid).get()

			new_data = request.get_json()

			location.name = new_data['name']
			location.address = new_data['address']
			location.facilities = new_data['facilities']
			location.coords = [new_data['lng'], new_data['lat']]

			opening_time_records = build_opening_times(opening_times_list=new_data['openingTimes'])
			location.openingTimes = opening_time_records

			try:
				location.save()

				location_data = convert_object_ids(document=location)
				response = (location_data, 200)

			except Exception as e:
				raise e

		except Exception as e:

			err_msg = "{} is not a valid id for a locaiton.".format(locationid)
			# err_msg += e

			response = (err_msg, 404)


	return response 


def location_delete(request, locationid=None):

	if locationid is None:
		response = ({"message": "locationid is required"}, 404)

	else:

		try:
			location = Location.objects(id=locationid).get().delete()
			response = ({'message': "location with id = {} was successfully removed".format(locationid)}, 204)

		except Exception as e:

			err_msg = "{} is not a valid id for a locaiton.".format(locationid)
			# err_msg += e

			response = (err_msg, 404)


	return response 



