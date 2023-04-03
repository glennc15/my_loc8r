angular.module('myLoc8rApp', []);

var _isNumeric = function (n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
};

var myLoc8rData = function($http) {
	var locationByCoords = function(lat, lng) {
		return $http.get('/api/locations?lng=' + lng + '&lat=' + lat + '&maxDistance=5');

	};

	return {locationByCoords: locationByCoords};
};


var geolocation = function() {
	var getPosition = function(cbSuccess, cbError, cbNoGeo) {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(cbSuccess, cbError);
		}
		else {
			cbNoGeo();
		}
	
	};


	return {getPosition: getPosition};
};


var formatDistance = function () {
	return function (distance) {
		var numDistance, unit;
		
		if (distance && _isNumeric(distance)){		
			if (distance > 1) {
				numDistance = parseFloat(distance).toFixed(1);
				unit = 'km';
			
			} else{
				numDistance = parseInt(distance * 1000, 10);
				unit = 'm';
			}

			return numDistance + unit;

		} else {
			return "?";
		
		}

	};
};

var ratingStars = function() {
	return {
		scope: {
			thisRating: '=rating'
		},
		templateUrl: '/angular/rating-stars.html'
	};

};

var locationListCtrl = function($scope, myLoc8rData, geolocation) {
	$scope.message = "Checking your location";

	$scope.getData = function(position) {
		$scope.message = "Searching for nearby places";

		var lat = position.coords.latitude;
		var lng = position.coords.longitude;

		myLoc8rData.locationByCoords(lat, lng)
			.success(function(data){
				$scope.message = data.length > 0 ? '' : "No locations found near you";
				// convert the facilities string into an array:
				console.log('data.length = ' + data.length);
				
				for (var i=0; i < data.lenght; i++) {
					console.log(data[i].facilities)
					data[i].facilities = data[i].facilities.split(',');
					// console.log(data[i])
				}

				$scope.data = {locations: data};
			})
			.error(function(e){
				$scope.message = "Sorry, something's gone wrong";
				
				console.log(e);
			});

	};

	$scope.showError = function(error) {
		$scope.$apply(function() {
			$scope.message = error.message;
		});
	};


	$scope.noGeo = function() {
		$scope.$apply(function() {
			$scope.message = "Geolocation not supported by this browser";
		});
	};

	geolocation.getPosition($scope.getData, $scope.showError, $scope.noGeo);


};


angular
	.module('myLoc8rApp')
	.controller('locationListCtrl', locationListCtrl)
	.filter('formatDistance', formatDistance)
	.directive('ratingStars', ratingStars)
	.service('myLoc8rData', myLoc8rData)
	.service('geolocation', geolocation);





	// $scope.data = {locations: myLoc8rData};

	// {
	// 	// message: null,
	// 	locations: [

	// 		{
	// 			"_id": "64104bfdc44df084085dbce6",
	// 			"address": " 7890 Walnut Street",
	// 			"dist_calc": 0.02181148800755852,
	// 			"facilities": "Espresso Machines".split(','),
	// 			"lat": 51.45524590032252,
	// 			"lng": -0.9690530959245162,
	// 			"name": "Daily Grind Coffee Co. ",
	// 			"openingTimes": [
	// 				{
	// 					"_id": "64104bfdc44df084085dbce5",
	// 					"closed": false,
	// 					"closing": "5:00pm",
	// 					"days": "Monday - Sunday",
	// 					"opening": "9:00am"
	// 				}
	// 			],
	// 			"rating": 0,
	// 			"reviews": []
	// 		},
  	// 		{
	// 		    "_id": "64104bfdc44df084085dbd05",
	// 		    "address": " 1234 Willow Street",
	// 		    "dist_calc": 0.22245244975528514,
	// 		    "facilities": "Espresso Machines".split(','),
	// 		    "lat": 51.45704495334908,
	// 		    "lng": -0.9688731201234213,
	// 		    "name": "The Coffee Spot ",
	// 		    "openingTimes": [
	// 				{
	// 					"_id": "64104bfdc44df084085dbd04",
	// 					"closed": false,
	// 					"closing": "10:00pm",
	// 					"days": "Monday - Sunday",
	// 					"opening": "7:00am"
	// 				}
	// 		    ],
	// 		    "rating": 5,
	// 		    "reviews": []
	// 		},
	// 		{
	// 			"_id": "64104bfec44df084085dbd26",
	// 			"address": " 7890 Maplewood Avenue",
	// 			"dist_calc": 0.39659583063468634,
	// 			"facilities": "Tea Selection,Specialty Drinks,Espresso Machines".split(','),
	// 			"lat": 51.45859360358829,
	// 			"lng": -0.9684789324813462,
	// 			"name": "The Coffee Collective ",
	// 			"openingTimes": [
	// 				{
	// 					"_id": "64104bfec44df084085dbd25",
	// 					"closed": false,
	// 					"closing": "10:00pm",
	// 					"days": "Monday - Sunday",
	// 					"opening": "7:00am"
	// 				}
	// 			],
	// 			"rating": 3,
	// 			"reviews": []
	// 		}
	// 	]

	// }


















































