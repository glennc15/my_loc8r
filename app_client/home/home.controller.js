(function() {


function homeCtrl ($scope, $filter, myLoc8rData, geolocation, mapHelpers, testData) {

	// import 'mapbox-gl/dist/mapbox-gl.css'; 

	
	var vm = this;

	vm.pageHeader = {
		title: 'myLoc8r',
		strapline: "Find places to work with wifi near you!"
	};

	vm.sidebar = {
		content: "Looking for wifi and a seat? myLoc8r helps you find places to work when out and about. Perhaps with coffee, cake or a pint? Let myLoc8r help you find the place you're looking for."
	};

	vm.message = "Checking your location";


	var addMap = function (locations, longitude, latitude){

		mapboxgl.accessToken = 'pk.eyJ1IjoiZ2xlbm5jMTUiLCJhIjoiY2xnNWJtajhxMDF3MjNrcGN0eWo2YzV5MyJ9.HQvXRdwCwWGYGa36rxEqgQ';


		const map = new mapboxgl.Map({
			container: 'map-locations', // container ID
			// Choose from Mapbox's core styles, or make your own style with Mapbox Studio
			style: 'mapbox://styles/mapbox/streets-v12', // style URL
			center: [longitude, latitude], // starting center in [lng, lat]
			// zoom: 1 // starting zoom
		});


		locations.forEach(function(location, index){
			const el = document.createElement('div');
			el.className = 'marker';

			// console.log(index + ": " + location.lng + ", " + location.lat);

			new mapboxgl
				.Marker(el)
				.setLngLat([location.lng, location.lat])
				.setPopup(
					new mapboxgl.Popup({ offset: 0}) // add popups
						.setHTML(`<h8>${location.name}</h8><p><small>${location.address}</small></p>`)				

				)
				.addTo(map);

		});


		// console.log("start longitude = " + longitude);
		// console.log("start latitude = " + latitude);


		// var map_bounds = mapHelpers.getBounds(longitude, latitude, 5);
		// console.log('map_bounds = ' + map_bounds);

		map.fitBounds(mapHelpers.getBounds(longitude, latitude, 2.6));

	};



	var processData = function(data, longitude, lattitude) {

		// console.log("data = " + JSON.stringify(data));
		// console.log('data.length = ' + data.length);
		// console.log(typeof data);

		vm.message = data.length > 0 ? '' : "No locations found near you";

		

		var facilities = [];

		// facilities come from the api as a string with each facility
		// seperated by a ',', the view expects facilities to be an
		// array of strings. So converting facilties to the correct format.

		// And the view expects a .distance value but the api send
		// a .dist_calc. So instead of updating the view I'm adding .distance.
		data.forEach(function(location){

			// console.log("location.facilities = " + JSON.stringify(location.facilities));

			location.facilities.split(',').forEach(function(facility){
				facilities.push(facility);
			});

			location.facilities = location.facilities.split(',');
			location.distance = location.dist_calc;
			location.num_reviews = location.reviews.length;

			// find the top review and make a brief summary of the review text:
			var top_review = location.reviews.sort(function(a, b) {
				return a.rating - b.rating;

			}).at(-1);


			location.review_summary = '"' + top_review.review_text.split(' ').slice(0, 7).join(' ') + '..."';

			// determine if the location is open or closed:
			location.is_open = $filter('isOpenNow')(location.openingTimes);

			// console.log("location.is_open = " + location.is_open);



		});

		// create a set of all facilities to use a filters:
		facilities = new Set(facilities);
		facilities = Array.from(facilities);
		facilities.sort(function(a, b) {
			a = a.charCodeAt(0);
			b = b.charCodeAt(0);

			var result = a - b;

			return result;
		});


		facility_filters = new Array;

		facilities.forEach(function(facility){
			facility_filters.push({
				value: facility,
				model: ('checkbox' + facility.split(' ').join('')),
				id: ('idCheckbox' + facility.split(' ').join('')),
			});
		});

		// console.log("facility_filters: " + JSON.stringify(facility_filters));

		vm.facilityFiltersData = facility_filters;

		// vm.facilitiesFilters = '';
		vm.facilitiesFilters = new Array;

		vm.data = {locations: data};

		vm.total_locations = data.length;

	};

	vm.filterChange = function(checkBox, this_filter) {
		if (checkBox) {
			// adding a facility filter
			vm.facilitiesFilters.push(this_filter)


		} else {
			// removeing a facility filter
			vm.facilitiesFilters = new Array;

			vm.facilityFiltersData.forEach(function(filter){
				if (filter.model==true) {
					vm.facilitiesFilters.push(filter.value);
				}

			});
		}
	};

	vm.getData = function(position) {
		vm.message = "Searching for nearby places";

		var lat = position.coords.latitude;
		var lng = position.coords.longitude;

		// get locations from the API and prepare the data for the view
		myLoc8rData.locationByCoords(lat, lng)
			.success(function(data){
				// processData(testData.locations());
				processData(data);
				addMap(vm.data.locations, lng, lat);

				// console.log(JSON.stringify(vm.data.locations));

			})
			.error(function(e){
				vm.message = "Sorry, something's gone wrong";
				console.log(e);
				
			});

		// // this is only for front end testing/development. It's static
		// // data from the service and is quicker than hitting the API
		// // everytime a front end change is made.

		// $scope.$apply(function () {
		// 	processData(testData.locations());
		// 	addMap(vm.data.locations, lng, lat);
		// });

		
		

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