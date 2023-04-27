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


// request.headers=Host: 127.0.0.1:5000
// User-Agent: python-requests/2.28.1
// Accept-Encoding: gzip, deflate, br
// Accept: */*
// Connection: keep-alive
// Content-Length: 131
// Content-Type: application/json
// Authorization: Basic ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SmZhV1FpT2lJMk5EUmhNMkkxTm1NMU5ERXdPVFkxWTJSbU1XWXhNRFVpTENKbGJXRnBiQ0k2SW0xMmIyOXlhR1ZsYzBCb2IzUnRZV2xzTG1OdmJTSXNJbTVoYldVaU9pSk5ZV1JwYzI5dUlGWnZiM0pvWldWeklpd2laWGh3SWpveE5qZ3pNVFkyTURVMGZRLk5wc2hnNDlSRG9HZVh2WGtPLXlTR29GZVNFTUVtWlZtd3hTTmVNYzNyTWc6Tm9uZQ==


// username: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2NDRhM2I1NmM1NDEwOTY1Y2RmMWYxMDUiLCJlbWFpbCI6Im12b29yaGVlc0Bob3RtYWlsLmNvbSIsIm5hbWUiOiJNYWRpc29uIFZvb3JoZWVzIiwiZXhwIjoxNjgzMTY2MDU0fQ.Npshg49RDoGeXvXkO-ySGoFeSEMEmZVmwxSNeMc3rMg
// password: None
// PUT: api_review_update(44a3b56c5410965cdf1f104, 644a3b56c5410965cdf1f106)




angular
	.module('myLoc8rApp')
	.service('myLoc8rData', myLoc8rData);


})();