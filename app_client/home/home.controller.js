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

	vm.message = "Searching for locations near you";

	var updateMapMarkers = function(){
		addMapLocations();
	};


	var getCurrentLocations = function() {

		var locations = new Array;

		// build map points for each filtered location:
		$filter('facilitiesFilter')(vm.data.locations, vm.facilitiesFilters).forEach(function(location){
			locations.push({
				'type': 'Feature',
				'properties': {
					'description':('<strong>' + location.name + '</strong><p>' + location.address + '</p>')
				},
				'geometry': {
					'type': 'Point',
					'coordinates': [location.lng, location.lat]
				}
			});

		});

		return locations;


	}

	var addMapLocations = function(){

		vm.map.removeLayer('locations');
		vm.map.removeSource('locations');

		vm.map.addSource('locations', {
			'type': 'geojson',
			'data': {
				'type': 'FeatureCollection',
				'features': getCurrentLocations()
			}
		});

		vm.map.addLayer({
			'id': 'locations',
			'type': 'circle',
			'source': 'locations',
			'paint': {
				'circle-color': '#4264fb',
				'circle-radius': 6,
				'circle-stroke-width': 2,
				'circle-stroke-color': '#ffffff'
			}
		});

	};

	var addMap = function (locations, longitude, latitude){

		mapboxgl.accessToken = 'pk.eyJ1IjoiZ2xlbm5jMTUiLCJhIjoiY2xnNWJtajhxMDF3MjNrcGN0eWo2YzV5MyJ9.HQvXRdwCwWGYGa36rxEqgQ';


		const map = new mapboxgl.Map({
			container: 'map-locations', // container ID
			// Choose from Mapbox's core styles, or make your own style with Mapbox Studio
			style: 'mapbox://styles/mapbox/streets-v12', // style URL
			center: [longitude, latitude], // starting center in [lng, lat]
			// zoom: 1 // starting zoom
		});

		// sets the map view area:
		map.fitBounds(mapHelpers.getBounds(longitude, latitude, 2.6));

		// add a current location marker:
		const currentLocationMarker = new mapboxgl.Marker({color: 'red', scale: .5})
			.setLngLat([longitude, latitude])
			.addTo(map);


		// add locations to the map:
		map.on('load', function() {
			map.addSource('locations', {
				'type': 'geojson',
				'data': {
					'type': 'FeatureCollection',
					'features': getCurrentLocations()
				}
			});

			map.addLayer({
				'id': 'locations',
				'type': 'circle',
				'source': 'locations',
				'paint': {
					'circle-color': '#4264fb',
					'circle-radius': 6,
					'circle-stroke-width': 2,
					'circle-stroke-color': '#ffffff'
				}
			});

			// Create a popup, but don't add it to the map yet.
			const popup = new mapboxgl.Popup({
				closeButton: false,
				closeOnClick: false
			});


			map.on('mouseenter', 'locations', (e) => {
				// Change the cursor style as a UI indicator.
				map.getCanvas().style.cursor = 'pointer';
				 
				// Copy coordinates array.
				const coordinates = e.features[0].geometry.coordinates.slice();
				const description = e.features[0].properties.description;
				 
				// Ensure that if the map is zoomed out such that multiple
				// copies of the feature are visible, the popup appears
				// over the copy being pointed to.
				while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
					coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
				}
				 
				// Populate the popup and set its coordinates
				// based on the feature found.
				popup.setLngLat(coordinates).setHTML(description).addTo(map);
			});
				 
			map.on('mouseleave', 'locations', () => {
				map.getCanvas().style.cursor = '';
				popup.remove();
			});





		});

		vm.map = map;
		
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

		// create a set of all facilities to use a filters. Converting to a
		// set removes all duplicate facilties:
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

		// vm.total_locations = data.length;



		

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

		updateMapMarkers();



	};


	vm.clearFilters = function() {
		// console.log("vm.clearFilters");

		// set all the filters to unchecked (false)
		vm.facilityFiltersData.forEach(function(filter){
			filter.model = false;
		});
		
		vm.facilitiesFilters = new Array;

		updateMapMarkers();

	}




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
				// processData(testData.locations());
				processData(data);
				addMap(vm.data.locations, lng, lat);

				if (vm.data.locations.length > 0){
					vm.showSpinner = false;
					vm.showLocations = true;
				}

			})
			.error(function(e){
				vm.message = "Sorry, something's gone wrong";
				vm.showSpinner = false;

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
			vm.showSpinner = false;
		});
	};


	vm.noGeo = function() {
		$scope.$apply(function() {
			vm.message = "Geolocation not supported by this browser";
			vm.showSpinner = false;

		});
	};

	geolocation.getPosition(vm.getData, vm.showError, vm.noGeo);


};


angular
	.module('myLoc8rApp')
	.controller('homeCtrl', homeCtrl);

})();