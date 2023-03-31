(function() {

var myLoc8rData = function($http, authentication) {
	var locationByCoords = function(lat, lng) {
		return $http.get('/api/locations?lng=' + lng + '&lat=' + lat + '&maxDistance=5');

	};

	var locationById = function (locationid) {
		return $http.get('/api/locations/' + locationid);
	};

	var addReviewById = function(locationid, data){

		console.log("POST data: " + JSON.stringify(data));

		return $http.post('/api/locations/' + locationid + '/reviews', data, {headers: {
			Authorization: 'Bearer ' + authentication.getToken()
		}});
	}

	return {
		locationByCoords: locationByCoords,
		locationById: locationById,
		addReviewById: addReviewById
	};
	
};


angular
	.module('myLoc8rApp')
	.service('myLoc8rData', myLoc8rData);


})();