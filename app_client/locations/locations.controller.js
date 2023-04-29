(function() {


function locationsCtrl ($scope, $filter, myLoc8rData, geolocation, mapHelpers) {
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

		// set the locations data for use but the view:
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

		// get locations from the API and prepare the data for the view
		myLoc8rData.locationByCoords(lat, lng)
			.success(function(data){

				processData(data.data);
				vm.map = mapHelpers.createMap(vm.data.locations, lng, lat, 2.6, data.map_key);

				if (vm.data.locations.length > 0){
					// vm.showWelcome = false;
					vm.showSpinner = false;
					vm.showLocations = true;
				}

			})
			.error(function(e){
				vm.message = "Sorry, something's gone wrong. Please try again.";
				vm.showSpinner = false;

				console.log(e);
				
			});		

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


angular
	.module('myLoc8rApp')
	.controller('locationsCtrl', locationsCtrl);

})();



