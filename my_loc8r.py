from flask import Flask 


app = Flask(__name__)

@app.route('/')
def locations():
	return "<p>Locations</p>"


@app.route('/location/<locationid>')
def location_details(locationid):
	return "<p>Location Details for {}!</p>".format(locationid)


@app.route('/location/<locationid>/review/new')
def add_loc_review(locationid):
	return "<p>Add a review for Location = {}!</p>".format(locationid)


@app.route('/about')
def about():
	return '<p>About Page</p>'