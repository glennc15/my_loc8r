(function() {


function homeCtrl ($scope, myLoc8rData, geolocation) {
	
	var vm = this;

	vm.pageHeader = {
		title: 'myLoc8r',
		strapline: "Find places to work with wifi near you!"
	};

	vm.sidebar = {
		content: "Looking for wifi and a seat? Loc8r helps you find places to work when out and about. Perhaps with coffee, cake or a pint? Let Loc8r help you find the place you're looking for."
	};

	vm.message = "Checking your location";


	vm.getData = function(position) {
		vm.message = "Searching for nearby places";

		var lat = position.coords.latitude;
		var lng = position.coords.longitude;

		// var postions_timestamp = position.timestamp;

		// console.log("postion.coords attributes:");
		// for (var key in position.coords) {
		// 	if (position.coords.hasOwnProperty(key)) {
		// 		console.log(key);
		// 	}

		// }



		// console.log("postions_timestamp = "+postions_timestamp)


		vm.ratingFilter = function(value) {
			console.log("value = " + value);

			if (value >= 1 && value <= 5) {
				return true;
			} else {
				return false;
			}


		};

		vm.myFilter = function(value, index, array) {


			console.log("value = " + JSON.stringify(value));
			console.log("index = " + index);
			console.log("array = " + array);

			var textFilter = '1'

			if (value.name.includes(textFilter) || value.address.includes(textFilter) || value.rating.toString().includes(textFilter)) {
				return true ;

			} else {
				return false;
			};


		

		};

		myLoc8rData.locationByCoords(lat, lng)
			.success(function(data){
				vm.message = data.length > 0 ? '' : "No locations found near you";
	
				
				// facilities come from the api as a string with each facility
				// seperated by a ',', the view expects facilities to be an
				// array of strings. So converting facilties to the correct format.

				// And the view expects a .distance value but the api send
				// a .dist_calc. So instead of updating the view I'm adding .distance.
				data.forEach(function(location){
					location.facilities = location.facilities.split(',');
					location.distance = location.dist_calc;
				});

				vm.data = {locations: data};
			})
			.error(function(e){
				vm.message = "Sorry, something's gone wrong";
				console.log(e);
				
			});

	};

	vm.showError = function(error) {
		$scope.$apply(function() {
			vm.message = error.message;
		});
	};


	vm.noGeo = function() {
		$scope.$apply(function() {
			vm.message = "Geolocation not supported by this browser";
		});
	};

	geolocation.getPosition(vm.getData, vm.showError, vm.noGeo);


};


angular
	.module('myLoc8rApp')
	.controller('homeCtrl', homeCtrl);

})();