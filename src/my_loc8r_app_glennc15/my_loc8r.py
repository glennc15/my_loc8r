from flask import Flask, request, g, send_from_directory 
from flask_mongoengine import MongoEngine
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from urllib.parse import urlparse
from dotenv import load_dotenv


from werkzeug.utils import secure_filename
import os 



# from .controllers.locations_api_controller import LocationsAPIController
from my_loc8r_app_glennc15.app_api.controllers.locations_api_controller import LocationsAPIController
from my_loc8r_app_glennc15.app_api.controllers.reviews_api_controller import ReviewsAPIController
from my_loc8r_app_glennc15.app_api.controllers.users_api_controller import UsersAPIController
from my_loc8r_app_glennc15.app_api.models.user_model import Users



import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete

def create_app(test_config=None):

	app = Flask(__name__, 
		# template_folder='app_server/templates',
		static_folder='app_client',
		static_url_path=''  
	)


	load_dotenv()

	# if os.environ.get("TESTING"):
	# 	# local testing:
	# 	app.config['MONGODB_SETTINGS'] = [
	# 		{
	# 			'db': 'myLoc8r',
	# 			'host': '192.168.1.2',
	# 			'port': 27017,
	# 			'alias': "default"
	# 		}
	# 	]


	# else:
	# 	app.config['MONGODB_SETTINGS'] = [
	# 		{
	# 			'db': 'myLoc8r',
	# 			'host': os.environ.get("MONGO_URI"),
	# 		}
	# 	]


	print("os.environ.get(MONGO_URI) = {}".format(os.environ.get("MONGO_URI")))

	# app.config['MONGODB_SETTINGS'] = [
	# 	{
	# 		'db': 'myLoc8r',
	# 		'host': '192.168.1.2',
	# 		'port': 27017,
	# 		'alias': "default"
	# 	}
	# ]

	app.config['MONGODB_HOST'] = os.environ.get("MONGO_URI")



	# check if the profiles directory exists and if not then create it:
	profiles_path = os.path.join(os.getcwd(), 'profiles')

	if not os.path.exists(profiles_path):
		os.mkdir(profiles_path)


	# UPLOAD_FOLDER = '/Users/glenn/Documents/GettingMEAN/my_loc8r/profiles'
	UPLOAD_FOLDER = profiles_path
	ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

	db = MongoEngine()
	db.init_app(app)


	# authorizations: using basic and token authorization:
	basic_auth = HTTPBasicAuth()
	token_auth = HTTPTokenAuth(scheme='Bearer')
	auth = MultiAuth(basic_auth, token_auth)


	# -------------------------------------------------------------------------------
	# app_client (SPA) routers:

	@app.route('/', defaults={'urlpath': ''})
	@app.route('/<path:urlpath>')
	def catch_all(urlpath):
		
		print("path: {}".format(urlpath))
		return app.send_static_file("index.html")

	@app.errorhandler(404)
	def not_found(e):
		# if url is for an api enpoint then return a 404. All other 404s return
		# the SPA index page:
		path = urlparse(request.url).path

		if '/api/' == path[0:5]:
			# api endpoint so send a 404:
			return ({'error': "{} not found".format(path)}, 404)

		else:
			return app.send_static_file("index.html")


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


			# add map api key:
			loc_api_controller.data = {
				'data': loc_api_controller.data,
				'map_key': os.environ.get('MAP_KEY')
			}


		# print("loc_api_controller.status_code = {}".format(loc_api_controller.status_code))
		# print("loc_api_controller.data = {}".format(loc_api_controller.data))


		# pdb.set_trace()


		return (loc_api_controller.data, loc_api_controller.status_code)


	@app.route('/api/locations/<locationid>', methods=['GET', 'PUT', 'DELETE'])
	def api_location(locationid):
		print("{}: api_location({})".format(request.method, locationid))

		loc_api_controller = LocationsAPIController()

		if request.method == 'GET':
			loc_api_controller.read_location_by_id(location_id=locationid)

			# add map api key:
			loc_api_controller.data = {
				'data': loc_api_controller.data,
				'map_key': os.environ.get('MAP_KEY')
			}

		if request.method == 'PUT':
			loc_api_controller.update_location(location_id=locationid, location_data=request.get_json())

		if request.method == 'DELETE':
			loc_api_controller.delete_location(location_id=locationid)


		return (loc_api_controller.data, loc_api_controller.status_code)



	# -------------------------------------------------------------------------------
	# Review routes:

	# authencation is requried for creating a review:
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

		return (review_api_controller.data, review_api_controller.status_code)



	@app.route('/api/locations/<locationid>/reviews/<reviewid>', methods=['GET'])
	def api_review_get(locationid, reviewid):
		print("{}: api_review_get({}, {})".format(request.method, locationid, reviewid))

		review_api_controller = ReviewsAPIController()
		review_api_controller.read_review(
			location_id=locationid, 
			review_id=reviewid
		)


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


		return (review_api_controller.data, review_api_controller.status_code)


	# -------------------------------------------------------------------------------
	# Authentication/User routes:

	@app.route('/api/register', methods=['POST'])
	def api_register():

		print(request.json)

		users_api_controller = UsersAPIController()
		users_api_controller.register(registration_data=request.json)

		print(users_api_controller.data)

		return (users_api_controller.data, users_api_controller.status_code)


	# user profile add pic endpoint:
	@app.route('/api/userprofile', methods=['POST'])
	@auth.login_required
	def api_add_profile():
		if 'file' not in request.files:
			return ({'error': "no file received"}, 400)

		file = request.files['file']

		if file.filename == '':
			return ({'error': "no file received"}, 400)


		if file:
			if allowed_file(file.filename):
				filename = secure_filename(file.filename)
				filename = "{}.{}".format(g.user.id, filename.rsplit('.', 1)[1].lower())

				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

				return ({'message': "profite pic successfully added"}, 200)

			else:
				return ({'error': "{} is not a valid file type".format(file.filename)}, 400)


	@app.route('/api/login', methods=['POST'])
	def api_login():
		print("api_login() request.headers={}".format(request.headers))

		users_api_controller = UsersAPIController()
		users_api_controller.login(login_data=request.json)
		
		return (users_api_controller.data, users_api_controller.status_code)



	@app.route('/api/profile/<userid>', methods=['GET'])
	def get_profile_pic(userid):
		print("{}:get_profile_pic({})".format(request.method, userid))
		
		if request.method == 'GET':
			filename_matched = False
			for this_file in os.listdir(app.config['UPLOAD_FOLDER']):
				try:
					filename, extension = this_file.rsplit('.', 1)

					if filename == userid:
						filename_matched = True 
						break 

				except Exception as e:
					pass 

			if filename_matched:
				print(this_file)

			else:
				this_file = 'default.png'


			return send_from_directory(app.config['UPLOAD_FOLDER'], this_file)



	# -------------------------------------------------------------------------------
	# Authencation Middleware:

	# @auth.error_handler
	@basic_auth.error_handler
	def auth_error(status):
	    return g.error_msg, status


	# @auth.verify_password
	@basic_auth.verify_password
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

	@token_auth.verify_token
	def verify_token(token):
		print("verify_token(token={})".format(token))

		return verify_password(username=token, password=None)


	# -------------------------------------------------------------------------------
	# Helpers:
	def allowed_file(filename):
		return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



	return app 

# if __name__ == "__main__":
	# app.run(debug=True)


