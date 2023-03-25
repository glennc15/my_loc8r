from flask import Flask, request
from flask_mongoengine import MongoEngine
# from flask import render_template
from flask_httpauth import HTTPBasicAuth



import my_loc8r.app_server.controllers.locations_ctrl as loc_ctrl

# import my_loc8r.app_api.controllers.locs_api_ctrl as locs_api_ctrl
from my_loc8r.app_api.controllers.locations_api_controller import LocationsAPIController
from my_loc8r.app_api.controllers.users_api_controller import UsersAPIController


# import my_loc8r.app_api.controllers.reviews_api_ctrl as reviews_api_ctrl 


import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete

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


auth = HTTPBasicAuth()



# *************************************************************
# app_server routers:

@app.route('/', methods=['GET'])
def locations():

	if request.method == 'GET':
		return loc_ctrl.locations_by_distance(request=request)



@app.route('/location/<locationid>', methods=['GET'])
def location_details(locationid):

	if request.method == 'GET':
		return loc_ctrl.location(request=request, location_id=locationid)


@app.route('/location/<locationid>/review/new', methods=['GET', 'POST'])
def add_loc_review(locationid):

	if request.method == 'GET':
		return loc_ctrl.add_review_page(request=request, location_id=locationid)


	elif request.method == 'POST':
		return loc_ctrl.add_review(request=request, location_id=locationid)



	# return "<p>Add a review for Location = {}!</p>".format(locationid)


@app.route('/about')
def about():
	return '<p>About Page</p>'


# *************************************************************


# *************************************************************
# api_server routers:


@auth.verify_password
def verify_password(username_or_token, password):
	return True


# Location routes:
@app.route('/api/locations', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_locations():

	loc_api_controller = LocationsAPIController()
	loc_api_controller.locations(request=request, location_id=None)

	print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
	print("loc_api_controller.data = {}".format(loc_api_controller.data))


	return (loc_api_controller.data, loc_api_controller.status_code)


@app.route('/api/locations/<locationid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_location(locationid):

	loc_api_controller = LocationsAPIController()
	loc_api_controller.locations(request=request, location_id=locationid)

	# print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
	# print("loc_api_controller.data = {}".format(loc_api_controller.data))

	return (loc_api_controller.data, loc_api_controller.status_code)




# Review routes:
@app.route('/api/locations/<locationid>/reviews', methods=['POST'])
@auth.login_required
def api_review_create(locationid):
	loc_api_controller = LocationsAPIController()
	loc_api_controller.reviews(request=request, location_id=locationid, review_id=None)

	print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
	print("loc_api_controller.data = {}".format(loc_api_controller.data))

	# pdb.set_trace()
	
	return (loc_api_controller.data, loc_api_controller.status_code)


# @app.route('/api/locations/<locationid>/reviews', methods=['GET', 'PUT', 'DELETE'])
# def api_review_indalid(locationid):
# 	# GET, PUT, DELETE are invalid for this endpoing and are handled by the controller
# 	loc_api_controller = LocationsAPIController()
# 	loc_api_controller.reviews(request=request, location_id=locationid, review_id=None)

# 	print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
# 	print("loc_api_controller.data = {}".format(loc_api_controller.data))

# 	# pdb.set_trace()
	
# 	return (loc_api_controller.data, loc_api_controller.status_code)


# @app.route('/api/locations/<locationid>/reviews/<reviewid>', methods=['GET', 'POST'])
@app.route('/api/locations/<locationid>/reviews/<reviewid>', methods=['GET'])
def api_review_get(locationid, reviewid):
	# A POST to this endpoint is invalid and is handled by the controller
	loc_api_controller = LocationsAPIController()
	loc_api_controller.reviews(request=request, location_id=locationid, review_id=reviewid)

	# print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
	# print("loc_api_controller.data = {}".format(loc_api_controller.data))


	return (loc_api_controller.data, loc_api_controller.status_code)


# authencation is requried for updateing or deleting a review:
@app.route('/api/locations/<locationid>/reviews/<reviewid>', methods=['PUT', 'DELETE'])
@auth.login_required
def api_review_update(locationid, reviewid):
	loc_api_controller = LocationsAPIController()
	loc_api_controller.reviews(request=request, location_id=locationid, review_id=reviewid)

	# print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
	# print("loc_api_controller.data = {}".format(loc_api_controller.data))


	return (loc_api_controller.data, loc_api_controller.status_code)






# Authentication routes:
@app.route('/api/register', methods=['POST'])
def api_register():
	users_api_controller = UsersAPIController()
	users_api_controller.register(request=request)

	# print("users_api_controller.status_code = {}".format(users_api_controller.status_code))
	# print("users_api_controller.data = {}".format(users_api_controller.data))

	return (users_api_controller.data, users_api_controller.status_code)


@app.route('/api/login', methods=['POST'])
def api_login():
	users_api_controller = UsersAPIController()
	users_api_controller.login(request=request)

	# print("users_api_controller.status_code = {}".format(users_api_controller.status_code))
	# print("users_api_controller.data = {}".format(users_api_controller.data))
	
	return (users_api_controller.data, users_api_controller.status_code)


# *************************************************************




