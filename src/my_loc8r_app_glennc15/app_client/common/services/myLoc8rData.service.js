(function() {
	
angular
	.module('myLoc8rApp')
	.service('myLoc8rData', myLoc8rData);

myLoc8rData.$inject = ["$http", "$window", "authentication", 'mapHelpers'];
function myLoc8rData($http, $window, authentication, mapHelpers) {
	

	var apiLocationByCoords = function(lat, lng) {

		return $http.get('/api/locations?lng=' + lng + '&lat=' + lat + '&maxDistance=5');

	};

	var addLocaitonBearings = function(locations) {

		locations.forEach(function(location) {
			// console.log(location);
			location.bearing = mapHelpers.getBearing(0, 0, location.lng, location.lat);
		});



		return locations;
	};


	var getCurrentLocation = function() {
		return JSON.parse($window.localStorage['myLoc8r-currentLocation']);
	}


	var saveCurrentLocation = function(lng, lat) {
		$window.localStorage['myLoc8r-currentLocation'] = JSON.stringify([lng, lat]);
	}



	var getLocationData = function() {

		var locations = JSON.parse($window.localStorage['myLoc8r-locations']);
		// locations = $window.localStorage['myLoc8r-locations'];

		return locations;

	};

	var saveLocationData = function(locaitonObjs) {
		$window.localStorage['myLoc8r-locations'] = JSON.stringify(locaitonObjs);

	}


	var updateLocations = function(locations, current_lng, current_lat) {

		locations.forEach(function(location) {
			var new_location_coords = mapHelpers.getEndpoint(current_lat, current_lng, location.bearing, location.dist_calc);
			location.lng = new_location_coords[0];
			location.lat = new_location_coords[1];
		});


		return locations;

	};



	var nearCurrentLocation = function(lng, lat, distance_trigger) {
		/*
		
		gets the distance between the current location and the supplied location.

		returns true if distance <= distance_trigger, else returns false.

		*/
		var currentLoc = getCurrentLocation();

		// console.log("currentLoc = " + currentLoc);
		// console.log("browserLoc = " + [lng, lat])

		var distance = mapHelpers.getDistance(currentLoc[0], currentLoc[1], lng, lat);

		// var distance = mapHelpers.getDistance(0, 0, 0, 0);


		// console.log("distance = " + distance);

		return (distance <= distance_trigger)

	};

	// 15May2023: rewritting locationByCoords(). The original plan of
	// generating random shops for a given current location is ultra slow
	// when using a production server and Mongo Atlas.  So now there are 45
	// locations in the database that are within 5 km from location
	// longitude/latitude =[0, 0].  All locations will be read from the
	// database and then new longitude/latitude coordinates will be
	// calculated so the locations are at the same distance/bearing from the
	// current location.  Then these new locations will be stored in the
	// browser for quick retrieval.

	// the following will be stored in the browswer:
	// myLoc8r-token: (controlled by the authentication service)
	// myLoc8r-locations: 
	// myLoc8r-lastUpdate: will reload locations if more than 1 day old (not implemented yet)
	// myLoc8r-mapKey:
	// myLoc8r-currentLocation: 


	var locationByCoords = function(lat, lng, forceUpdate=false) {

		return null;

	};



	var getMapKey = function() {
		return $window.localStorage['myLoc8r-mapKey'];
	};


	var locationById = function (locationid) {
		return $http.get('/api/locations/' + locationid);
	};

	
	var addReviewById = function(locationid, data){

		// console.log("POST data: " + JSON.stringify(data));

		authentication.currentUser();

		// console.log("token = " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2NDQ2MmRlNzFlNGViMWZkMzBlN2QxNzEiLCJlbWFpbCI6ImttZWppYTgxQGhvdG1haWwuY29tIiwibmFtZSI6IkthbWVrbyBNZWppYSIsImV4cCI6MTY4MzE0Mjk4OX0.Q_xodZAHRD65Rqko2ZpysiqMGP_5r8ds4N7enUMNTo4");
		// console.log("authentication.getToken() = " + authentication.getToken());


		// return $http.post('/api/locations/' + locationid + '/reviews', data, {headers: {
		// 	Authorization: authentication.getToken()
		// }});

		return $http.post('/api/locations/' + locationid + '/reviews', data, {headers: {
			Authorization: 'Bearer ' + authentication.getToken(),
			username: authentication.getToken(),
			password: null
		}});


	}

	return {
		locationByCoords: locationByCoords,
		locationById: locationById,
		addReviewById: addReviewById,
		getMapKey: getMapKey,
		apiLocationByCoords: apiLocationByCoords,
		addLocaitonBearings: addLocaitonBearings,
		updateLocations: updateLocations
	};
	
};


})();