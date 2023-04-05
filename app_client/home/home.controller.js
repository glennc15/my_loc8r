(function() {


function homeCtrl ($scope, $filter, myLoc8rData, geolocation) {
	
	var vm = this;

	vm.pageHeader = {
		title: 'myLoc8r',
		strapline: "Find places to work with wifi near you!"
	};

	vm.sidebar = {
		content: "Looking for wifi and a seat? myLoc8r helps you find places to work when out and about. Perhaps with coffee, cake or a pint? Let myLoc8r help you find the place you're looking for."
	};

	vm.message = "Checking your location";


	vm.filterChange = function(checkBox, this_filter) {
		console.log("checkBox = " + checkBox);

		if (checkBox) {
			console.log("add filter = " + this_filter);
			vm.facilitiesFilters.push(this_filter)


		} else {
			console.log("remove filter = " + this_filter);
			vm.facilitiesFilters = new Array;

			vm.facilityFiltersData.forEach(function(filter){
				console.log('filter.model = ' + filter.model);

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