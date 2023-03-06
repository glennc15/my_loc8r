from flask import Flask, request

# from flask import render_template

import my_loc8r.app_server.controllers.locations as loc 


# from jinja2 import Environment, FileSystemLoader
# template_dir = '/Users/glenn/Documents/GettingMEAN/my_loc8r/app_server/templates/'
# env = Environment(loader=FileSystemLoader(template_dir))


app = Flask(__name__, template_folder='app_server/templates')

@app.route('/', methods=['GET'])
def locations():

	if request.method == 'GET':

	# return "<p>Locations</p>"
	# return render_template('app_server/templates/hello.html')
		return loc.locations_by_distance(request=request)
		# return render_template('hello.html')



@app.route('/location/<locationid>')
def location_details(locationid):
	return render_template('hello.html', name=locationid)


@app.route('/location/<locationid>/review/new')
def add_loc_review(locationid):
	return "<p>Add a review for Location = {}!</p>".format(locationid)


@app.route('/about')
def about():
	return '<p>About Page</p>'