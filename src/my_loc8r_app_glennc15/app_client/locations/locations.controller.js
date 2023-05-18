(function() {


angular
	.module('myLoc8rApp')
	.controller('locationsCtrl', locationsCtrl);

locationsCtrl.$inject = ['$scope', '$filter', '$window', 'myLoc8rData', 'geolocation', 'mapHelpers'];
function locationsCtrl($scope, $filter, $window, myLoc8rData, geolocation, mapHelpers) {
	var vm = this;

	// when the page first loads the spinner is displayed and the Locations
	// are hidden till they are properly loaded from the API.
	vm.showSpinner = true;
	vm.showLocations = false;


	// helper function: gets the location data from the API and readies it for
	// the view.
	var processData = function(data, longitude, lattitude) {


		// No locations found near this location:
		vm.message = data.length > 0 ? '' : "No locations found near you";



		// facilities come from the api as a string with each facility
		// seperated by a ',', the view expects facilities to be an
		// array of strings. So converting facilties to the correct format.

		// And the view expects a .distance value but the api send
		// a .dist_calc. So instead of updating the view I'm adding .distance.

		var facilities = [];
		data.forEach(function(location){


			// console.log("location.facilities = " + location.facilities);

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

			// console.log("this location = " + JSON.stringify(location));

		});

		// Setting up the location filters. Create a set of all facilities to
		// use a filters. Converting to a set removes all duplicate facilties:
		facilities = new Set(facilities);
		facilities = Array.from(facilities);
		facilities.sort(function(a, b) {
			a = a.charCodeAt(0);
			b = b.charCodeAt(0);

			var result = a - b;

			return result;
		});


		// Filter initializations:
		facility_filters = new Array;

		facilities.forEach(function(facility){
			facility_filters.push({
				value: facility,
				model: ('checkbox' + facility.split(' ').join('')),
				id: ('idCheckbox' + facility.split(' ').join('')),
			});
		});

		vm.facilityFiltersData = facility_filters;

		// .facilitesFilters is used by Angularjs to filter locations by
		//  facility tags entered into this array. The array is initialized
		//  to empty so all locations are displayed:
		vm.facilitiesFilters = new Array;

		// set the locations data for use by the view:
		vm.data = {locations: data};
		vm.total_locations = data.length;


	};

	// helper function; called when a filter is checked/unchecked. When a
	// filter is checked the filter tag gets added to .facilitiesFilers
	// array. Then this array is used by angularjs to only show locations
	// that contain that filter tag. When a filter is unchecked then that
	// facility tag is removed from .facilitiesFilers
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

		// update the map to show filtered locations:
		var mapLocations = $filter('facilitiesFilter')(vm.data.locations, vm.facilitiesFilters);
		mapHelpers.updateMap(vm.map, mapLocations);

	};

	// helper function; clears all filters so all locations are once again
	// visible.
	vm.clearFilters = function() {
		// console.log("vm.clearFilters");

		// set all the filters to unchecked (false)
		vm.facilityFiltersData.forEach(function(filter){
			filter.model = false;
		});
		
		vm.facilitiesFilters = new Array;

		// update the map to show filtered locations:
		var mapLocations = $filter('facilitiesFilter')(vm.data.locations, vm.facilitiesFilters);
		mapHelpers.updateMap(vm.map, mapLocations);

	}




	// This processed the GeoLocation data from the browser and gets nearest
	// locations from the API: 
	vm.getData = function(position) {
		vm.message = "Searching for nearby places";

		vm.showLocations = false;
		vm.showSpinner = true;

		var lat = position.coords.latitude;
		var lng = position.coords.longitude;

		vm.lat = lat;
		vm.lng = lng;

		// locations are stored in the session. If there are no locations
		// stored in the session then get locations from the api and store
		// them in the session.
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
					locations = myLoc8rData.updateLocations(locations, lng, lat);
					$window.sessionStorage['myLoc8r-locations'] = JSON.stringify(locations);
					$window.sessionStorage['myLoc8r-mapKey'] = JSON.stringify(data.map_key);

					// checks if each location is currently open, formats
					// facilities, and builds the filters.
					processData(locations);
					vm.map = mapHelpers.createMap(vm.data.locations, lng, lat, 2.6, data.map_key);

					if (vm.data.locations.length > 0){
						vm.showSpinner = false;
						vm.showLocations = true;

					} else {
						vm.message = "Oh no! We could not find any locations near you. Please try again later :(";
						vm.showSpinner = false;

					}

				})
				.error(function(e){
					vm.message = "Sorry, something's gone wrong. Please try again.";
					vm.showSpinner = false;

					console.log(e);
					
				});		


		// Locations are stored in the session so read the location from
		// session and prepare the locations:
		} else {

			console.log("getting data from session");

			var locations = JSON.parse($window.sessionStorage['myLoc8r-locations']);
			const mapKey = JSON.parse($window.sessionStorage['myLoc8r-mapKey']);

			// update each location position so it's near the current
			// position, checks if each location is currently open, formats
			// facilities, and builds the filters.
			locations = myLoc8rData.updateLocations(locations, lng, lat);
			processData(locations);
			vm.map = mapHelpers.createMap(vm.data.locations, lng, lat, 2.6, mapKey);

			if (vm.data.locations.length > 0){
				$scope.$apply(function() {
					vm.showSpinner = false;
					vm.showLocations = true;

				});

			}
		}
	};


	// general error during location processing:
	vm.showError = function(error) {
		$scope.$apply(function() {
			vm.message = error.message;
			vm.showSpinner = false;
		});
	};


	// called if the brower doesn't support Geolocation service (or if the
	// user does not give location permission.)
	vm.noGeo = function() {
		$scope.$apply(function() {
			vm.message = "Geolocation not supported by this browser";
			vm.showSpinner = false;

		});
	};


	// Entry point: 
	// 
	// 1st it gets the current location using the browsers
	// location service (requires user permission). Once the GPS coordinates
	// are given by the brower then the nearest locations are displayed.
	geolocation.getPosition(vm.getData, vm.showError, vm.noGeo);


};




})();



