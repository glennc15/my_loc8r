(function() {
	
angular
	.module('myLoc8rApp')
	.service('myLoc8rData', myLoc8rData);

myLoc8rData.$inject = ["$http", "authentication"];
function myLoc8rData($http, authentication) {
	
	var locationByCoords = function(lat, lng) {
		return $http.get('/api/locations?lng=' + lng + '&lat=' + lat + '&maxDistance=5');

	};

	var locationById = function (locationid) {
		return $http.get('/api/locations/' + locationid);
	};

	
	var addReviewById = function(locationid, data){

		console.log("POST data: " + JSON.stringify(data));

		authentication.currentUser();

		console.log("token = " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2NDQ2MmRlNzFlNGViMWZkMzBlN2QxNzEiLCJlbWFpbCI6ImttZWppYTgxQGhvdG1haWwuY29tIiwibmFtZSI6IkthbWVrbyBNZWppYSIsImV4cCI6MTY4MzE0Mjk4OX0.Q_xodZAHRD65Rqko2ZpysiqMGP_5r8ds4N7enUMNTo4");
		console.log("authentication.getToken() = " + authentication.getToken());


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
		addReviewById: addReviewById
	};
	
};


})();