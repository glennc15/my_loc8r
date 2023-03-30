from flask import Flask, request, g 
from flask_mongoengine import MongoEngine
# from flask import render_template
from flask_httpauth import HTTPBasicAuth



# import my_loc8r.app_server.controllers.locations_ctrl as loc_ctrl

# import my_loc8r.app_api.controllers.locs_api_ctrl as locs_api_ctrl
from my_loc8r.app_api.controllers.locations_api_controller import LocationsAPIController
from my_loc8r.app_api.controllers.reviews_api_controller import ReviewsAPIController
from my_loc8r.app_api.controllers.users_api_controller import UsersAPIController

from my_loc8r.app_api.models.user_model import Users

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



# -------------------------------------------------------------------------------
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







# -------------------------------------------------------------------------------
# Location routes:

@app.route('/api/locations', methods=['GET', 'POST'])
def api_locations():
	print("{}: api_locations()".format(request.method))

	loc_api_controller = LocationsAPIController()


	if request.method == 'POST':
		loc_api_controller.create_location(location_data=request.get_json())


	if request.method == 'GET':
		loc_api_controller.read_locations_by_distance(parameters=request.args.to_dict())


	print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
	print("loc_api_controller.data = {}".format(loc_api_controller.data))


	# pdb.set_trace()


	return (loc_api_controller.data, loc_api_controller.status_code)


@app.route('/api/locations/<locationid>', methods=['GET', 'PUT', 'DELETE'])
def api_location(locationid):
	print("{}: api_location({})".format(request.method, locationid))

	loc_api_controller = LocationsAPIController()

	if request.method == 'GET':
		loc_api_controller.read_location_by_id(location_id=locationid)


	if request.method == 'PUT':
		loc_api_controller.update_location(location_id=locationid, location_data=request.get_json())


	if request.method == 'DELETE':
		loc_api_controller.delete_location(location_id=locationid)



	# loc_api_controller.locations(request=request, location_id=locationid)

	print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
	print("loc_api_controller.data = {}".format(loc_api_controller.data))

	return (loc_api_controller.data, loc_api_controller.status_code)



# -------------------------------------------------------------------------------
# Review routes:

@app.route('/api/locations/<locationid>/reviews', methods=['POST'])
@auth.login_required
def api_review_create(locationid):
	print("{}: api_review_create({})".format(request.method, locationid))

	review_api_controller = ReviewsAPIController()
	review_api_controller.create_review(
		location_id=locationid, 
		review_data=request.get_json(), 
		user=g.user
	)

	print("review_api_controller.status_code = {}".format(review_api_controller.status_code))
	print("review_api_controller.data = {}".format(review_api_controller.data))

	# pdb.set_trace()
	
	return (review_api_controller.data, review_api_controller.status_code)



@app.route('/api/locations/<locationid>/reviews/<reviewid>', methods=['GET'])
def api_review_get(locationid, reviewid):

	print("{}: api_review_get({}, {})".format(request.method, locationid, reviewid))

	review_api_controller = ReviewsAPIController()
	review_api_controller.read_review(
		location_id=locationid, 
		review_id=reviewid
	)

	print("review_api_controller.status_code = {}".format(review_api_controller.status_code))
	print("review_api_controller.data = {}".format(review_api_controller.data))

	return (review_api_controller.data, review_api_controller.status_code)


# authencation is requried for updateing or deleting a review:
@app.route('/api/locations/<locationid>/reviews/<reviewid>', methods=['PUT', 'DELETE'])
@auth.login_required
def api_review_update(locationid, reviewid):

	print("{}: api_review_update({}, {})".format(request.method, locationid, reviewid))
	
	review_api_controller = ReviewsAPIController()

	if request.method == "PUT":
		review_api_controller.update_review(
			location_id=locationid, 
			review_id=reviewid, 
			review_data=request.get_json(), 
			user=g.user
		)

	if request.method == 'DELETE':
		review_api_controller.delete_review(
			location_id=locationid, 
			review_id=reviewid,
			user=g.user
		)


	print("review_api_controller.status_code = {}".format(review_api_controller.status_code))
	print("review_api_controller.data = {}".format(review_api_controller.data))


	return (review_api_controller.data, review_api_controller.status_code)


# -------------------------------------------------------------------------------
# Authentication/User routes:

@app.route('/api/register', methods=['POST'])
def api_register():
	users_api_controller = UsersAPIController()
	users_api_controller.register(request=request)

	print("users_api_controller.status_code = {}".format(users_api_controller.status_code))
	print("users_api_controller.data = {}".format(users_api_controller.data))

	return (users_api_controller.data, users_api_controller.status_code)


@app.route('/api/login', methods=['POST'])
def api_login():
	users_api_controller = UsersAPIController()
	users_api_controller.login(request=request)

	print("users_api_controller.status_code = {}".format(users_api_controller.status_code))
	print("users_api_controller.data = {}".format(users_api_controller.data))
	
	return (users_api_controller.data, users_api_controller.status_code)



@app.route('/api/user/<userid>', methods=['PUT'])
def api_user():

	users_api_controller = UsersAPIController()
	users_api_controller.user_update(
		user_id=userid, 
		user_data=request.get_json()
	)
	

	print("users_api_controller.status_code = {}".format(users_api_controller.status_code))
	print("users_api_controller.data = {}".format(users_api_controller.data))
	
	return (users_api_controller.data, users_api_controller.status_code)



# -------------------------------------------------------------------------------
# Authencation Middleware:

@auth.error_handler
def auth_error(status):
    return g.error_msg, status


@auth.verify_password
def verify_password(username, password):

	user, error_msg = Users.verify_jwt(jwt_token=username)

	if isinstance(user, Users):
		g.user = user
		g.error_msg = None  
		return True

	else:
		g.user = None
		g.error_msg = error_msg  
		return False




