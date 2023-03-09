from flask import Flask, request
from flask_mongoengine import MongoEngine
# from flask import render_template

import my_loc8r.app_server.controllers.locations_ctrl as loc_ctrl

# import my_loc8r.app_api.controllers.locs_api_ctrl as locs_api_ctrl
from my_loc8r.app_api.controllers.locations_api_controller import LocationsAPIController

import my_loc8r.app_api.controllers.reviews_api_ctrl as reviews_api_ctrl 




# from jinja2 import Environment, FileSystemLoader
# template_dir = '/Users/glenn/Documents/GettingMEAN/my_loc8r/app_server/templates/'
# env = Environment(loader=FileSystemLoader(template_dir))



app = Flask(__name__, template_folder='app_server/templates')
app.config['MONGODB_SETTINGS'] = [
	{
		'db': 'myLoc8r',
		'host': '192.168.1.2',
		'port': 27017,
		'alias': "default"
	}
]

db = MongoEngine()
db.init_app(app)



# *************************************************************
# app_server routers:

@app.route('/', methods=['GET'])
def locations():

	if request.method == 'GET':
		return loc_ctrl.locations_by_distance(request=request)



@app.route('/location/<locationid>', methods=['GET'])
def location_details(locationid):

	if request.method == 'GET':
		return loc_ctrl.location(request=request)


@app.route('/location/<locationid>/review/new')
def add_loc_review(locationid):
	return "<p>Add a review for Location = {}!</p>".format(locationid)


@app.route('/about')
def about():
	return '<p>About Page</p>'


# *************************************************************


# *************************************************************
# api_server routers:

# Location routes:
@app.route('/api/locations', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_locations():

	loc_api_controller = LocationsAPIController()
	loc_api_controller.locations(request=request, location_id=None)

	# print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
	# print("loc_api_controller.data = {}".format(loc_api_controller.data))


	return (loc_api_controller.data, loc_api_controller.status_code)


@app.route('/api/locations/<locationid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_location(locationid):

	loc_api_controller = LocationsAPIController()
	loc_api_controller.locations(request=request, location_id=locationid)

	# print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
	# print("loc_api_controller.data = {}".format(loc_api_controller.data))

	return (loc_api_controller.data, loc_api_controller.status_code)




# Review routes:
@app.route('/api/locations/<locationid>/reviews', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_review_create(locationid):
	loc_api_controller = LocationsAPIController()
	loc_api_controller.reviews(request=request, location_id=locationid, review_id=None)

	return (loc_api_controller.data, loc_api_controller.status_code)



	# if request.method == 'POST':
	# 	return reviews_api_ctrl.review_create(request=request)


@app.route('/api/locations/<locationid>/reviews/<reviewid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_review_CRUD(locationid, reviewid):
	loc_api_controller = LocationsAPIController()
	loc_api_controller.reviews(request=request, location_id=locationid, review_id=reviewid)

	return (loc_api_controller.data, loc_api_controller.status_code)

	# if request.method == 'GET':
	# 	return reviews_api_ctrl.review_read(request=request, locationid=locationid, reviewid=reviewid)

	# if request.method == 'PUT':
	# 	return reviews_api_ctrl.review_update(request=request, locationid=locationid, reviewid=reviewid)

	# if request.method == 'DELETE':
	# 	return reviews_api_ctrl.review_delete(request=request, locationid=locationid, reviewid=reviewid)


# *************************************************************




