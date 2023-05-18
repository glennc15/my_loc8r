(function() {


angular
	.module('myLoc8rApp')
	.controller('locationDetailCtrl', locationDetailCtrl);


locationDetailCtrl.$inject = ['$routeParams', '$window', 'myLoc8rData', '$location', 'authentication', 'mapHelpers'];
function locationDetailCtrl($routeParams, $window, myLoc8rData, $location, authentication, mapHelpers) {

	var vm = this;

	vm.locationid = $routeParams.locationid;

	vm.isLoggedIn = authentication.isLoggedIn();

	vm.currentPath = "/" + $routeParams.locationid + "?lng=" + $routeParams.lng + "&lat=" + $routeParams.lat + "&dist=" + $routeParams.dist;

	// 18 May 2023: All locations are in local storage so retrieving the
	// location from local storage. No checking if locations exists in local
	// storage so there is definately room for imporvement.


	if ($window.sessionStorage['myLoc8r-locations'] == null) {

		myLoc8rData.apiLocationByCoords(0, 0)
			.success(function(data){
				console.log("getting data from api");

				// console.log("data.data instanceof Array =  " + (data.data instanceof Array));

				// add bearing data to the locations. This allows each
				// location coordinate to be updated near the current
				// position given by the browser. Then save the locations
				// and teh map key to local storage:
				var locations = myLoc8rData.addLocaitonBearings(data.data);
				locations = myLoc8rData.updateLocations(locations, $routeParams.lng, $routeParams.lat);
				$window.sessionStorage['myLoc8r-locations'] = JSON.stringify(locations);
				$window.sessionStorage['myLoc8r-mapKey'] = JSON.stringify(data.map_key);

				let location = locations.find(t => t._id === vm.locationid);

				// convert facilities to an array of strings for each facility:
				location.facilities =  location.facilities.split(',');


				// add author short name and format the timestamp to a moment:
				location.reviews.forEach(function(review) {
					review.authorShort = review.author.split(' ')[0] + ' ' + review.author.split(' ')[1][0];
					review.moment = moment(review.created_on).fromNow();
					review.created_on = new Date(review.created_on);

				});


				vm.data = {location: location};

				vm.pageHeader = {
					title: vm.data.location.name
				};

				var mapWindow = Math.ceil($routeParams.dist*10)/10;
				vm.map = mapHelpers.createMap([vm.data.location], $routeParams.lng, $routeParams.lat, mapWindow, data.map_key);




				// console.log("vm.data.locations instanceof Array =  " + (vm.data.locations instanceof Array));
				// console.log("vm.facilitiesFilters = " + JSON.stringify(vm.facilitiesFilters));
				// console.log("vm.facilityFiltersData = " + JSON.stringify(vm.facilityFiltersData));
				// console.log("vm.data.locations.length = " + JSON.stringify(vm.data.locations.length));
				// console.log("vm.data.locations[0] = " + JSON.stringify(vm.data.locations[0]));


			})
			.error(function(e){
				vm.message = "Sorry, something's gone wrong. Please try again.";
				vm.showSpinner = false;

				console.log(e);
				
			});		

	} else {

		console.log("vm.locationid = " + vm.locationid);

		var locations = JSON.parse($window.sessionStorage['myLoc8r-locations']);
		const mapKey = JSON.parse($window.sessionStorage['myLoc8r-mapKey']);

		let location = locations.find(t => t._id === vm.locationid);

		// convert facilities to an array of strings for each facility:
		location.facilities =  location.facilities.split(',');


		// add author short name and format the timestamp to a moment:
		location.reviews.forEach(function(review) {
			review.authorShort = review.author.split(' ')[0] + ' ' + review.author.split(' ')[1][0];
			review.moment = moment(review.created_on).fromNow();
			review.created_on = new Date(review.created_on);

		});


		vm.data = {location: location};

		vm.pageHeader = {
			title: vm.data.location.name
		};

		var mapWindow = Math.ceil($routeParams.dist*10)/10;
		vm.map = mapHelpers.createMap([vm.data.location], $routeParams.lng, $routeParams.lat, mapWindow, mapKey);

	}



	// var locations = JSON.parse($window.sessionStorage['myLoc8r-locations']);
	// const mapKey = JSON.parse($window.sessionStorage['myLoc8r-mapKey']);

	// let location = locations.find(t => t._id === vm.locationid);

	// // convert facilities to an array of strings for each facility:
	// location.facilities =  location.facilities.split(',');


	// // add author short name and format the timestamp to a moment:
	// location.reviews.forEach(function(review) {
	// 	review.authorShort = review.author.split(' ')[0] + ' ' + review.author.split(' ')[1][0];
	// 	review.moment = moment(review.created_on).fromNow();
	// 	review.created_on = new Date(review.created_on);

	// });


	// vm.data = {location: location};

	// vm.pageHeader = {
	// 	title: vm.data.location.name
	// };

	// var mapWindow = Math.ceil($routeParams.dist*10)/10;
	// vm.map = mapHelpers.createMap([vm.data.location], $routeParams.lng, $routeParams.lat, mapWindow, mapKey);


	// ################################################################# 

	// console.log("location = " + JSON.stringify(location));


	// myLoc8rData.locationById($routeParams.locationid)
	// 	.success(function(location) {

	// 		// facilities come from the api as a string with each facility
	// 		// seperated by a ',', the view expects facilities to be an
	// 		// array of strings. So converting facilties to the correct format.
	// 		location.data['facilities'] = location.data['facilities'].split(',');

	// 		vm.data = {location: location.data};

	// 		// author short name: [first name] [first initial in last name]
	// 		vm.data.location.reviews.forEach(function(review) {
	// 			review.authorShort = review.author.split(' ')[0] + ' ' + review.author.split(' ')[1][0];
	// 			review.moment = moment(review.created_on).fromNow();

	// 		});
			
	// 		vm.pageHeader = {
	// 			title: vm.data.location.name
	// 		};

	// 		var mapWindow = Math.ceil($routeParams.dist*10)/10;
	// 		vm.map = mapHelpers.createMap([vm.data.location], $routeParams.lng, $routeParams.lat, mapWindow, location.map_key);

	// 	})
	// 	.error(function(e) {
	// 		console.log(e);

	// 	});


};



})();






