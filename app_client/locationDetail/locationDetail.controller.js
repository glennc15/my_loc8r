(function() {

// var locationDetailCtrl = function($routeParams, myLoc8rData, $modal, $location, authentication, mapHelpers) {
var locationDetailCtrl = function($routeParams, myLoc8rData, $location, authentication, mapHelpers) {

	var vm = this;

	vm.locationid = $routeParams.locationid;

	vm.isLoggedIn = authentication.isLoggedIn();

	vm.currentPath = "/" + $routeParams.locationid + "?lng=" + $routeParams.lng + "&lat=" + $routeParams.lat + "&dist=" + $routeParams.dist;

	// $routeParams.lng, $routeParams.lat, $routeParams.dist

	// vm.locationPath = 

	vm.pageHeader = {
		title: "Location detail page"
	};


	// var myModal = document.getElementById('exampleModal')
	// var myInput = document.getElementById('myInput')

	// myModal.addEventListener('shown.bs.modal', function () {
	//   myInput.focus()
	// })


	var addMap = function (locationData, longitude, latitude, distance, map_api_key){

		mapboxgl.accessToken = map_api_key;

		const map = new mapboxgl.Map({
			container: 'map-locations', // container ID
			style: 'mapbox://styles/mapbox/streets-v12', // style URL
			center: [longitude, latitude], // starting center in [lng, lat]
		});

		// sets the map view area:
		map.fitBounds(mapHelpers.getBounds(longitude, latitude, (Math.ceil(distance*10)/10)));

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
					'features': [
						{
							'type': 'Feature',
							'properties': {
								'description':('<strong>' + locationData.name + '</strong><p>' + locationData.address + '</p>')
							},
							'geometry': {
								'type': 'Point',
								'coordinates': [locationData.lng, locationData.lat]
							}
						}
					]
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

			map.on('render', function() {
				map.resize();
			});

		});

		vm.map = map;
		
	};




	myLoc8rData.locationById($routeParams.locationid)
		.success(function(location) {

			// facilities come from the api as a string with each facility
			// seperated by a ',', the view expects facilities to be an
			// array of strings. So converting facilties to the correct format.
			location.data['facilities'] = location.data['facilities'].split(',');

			vm.data = {location: location.data};

			// author short name: [first name] [first initial in last name]
			vm.data.location.reviews.forEach(function(review) {
				review.authorShort = review.author.split(' ')[0] + ' ' + review.author.split(' ')[1][0];
				review.moment = moment(review.created_on).fromNow();

			});
			
			vm.pageHeader = {
				title: vm.data.location.name
			};

			// addMap(vm.data.location, $routeParams.lng, $routeParams.lat, $routeParams.dist, location.map_key);

		})
		.error(function(e) {
			console.log(e);

		});


		// vm.popupReviewForm = function() {
		// 	console.log("trying to open the review form!")
		// 	var modalInstance = $modal.open({
		// 		templateUrl: '/reviewModal/reviewModal.view.html',
		// 		controller: 'reviewModalCtrl as vm',
		// 		resolve: {
		// 			locationData: function() {
		// 				return {
		// 					locationid: vm.locationid,
		// 					locationName: vm.data.location.name
		// 				};
		// 			}
		// 		}
		// 	});


		// 	modalInstance.result.then(function(data){
		// 		vm.data.location.reviews.push(data);
				
		// 	});
		// };





};


angular
	.module('myLoc8rApp')
	.controller('locationDetailCtrl', locationDetailCtrl);

})();






