(function() {

angular
	.module('myLoc8rApp')
	.service('mapHelpers', mapHelpers);

function mapHelpers() {
	// helper function:
	var degrees2radians = function(degrees) {
		return degrees * Math.PI/180;
	};

	// helper function:
	var radians2degrees = function(radians) {
		return radians *  180 / Math.PI;
	};

	// helper function: takes a start longtude/latitude, bearing and distance
	// and calculates the destination longitude/latitude:
	var getEndpoint = function(lat1,lon1,bearing,d) {
		var R = 6371; 						// Radius of the Earth in km
		var brng = degrees2radians(bearing); // convert degrees to radians
		var lat1 = degrees2radians(lat1);    // Current lat point converted to radians
		var lon1 = degrees2radians(lon1);    // Current long point converted to radians
		var lat2 = Math.asin( Math.sin(lat1)*Math.cos(d/R) + Math.cos(lat1)*Math.sin(d/R)*Math.cos(brng));
		var lon2 = lon1 + Math.atan2(Math.sin(brng)*Math.sin(d/R)*Math.cos(lat1),Math.cos(d/R)-Math.sin(lat1)*Math.sin(lat2));
		var lat2 = radians2degrees(lat2);
		var lon2 = radians2degrees(lon2);
		
		return [lon2, lat2];

	};





	var getDistance = function (lon1, lat1, lon2, lat2) {

		// console.log("lon1 = " + lon1);
		// console.log("lat1 = " + lat1);

		// console.log("lon2 = " + lon2);
		// console.log("lat2 = " + lat2);


		const R = 6371; // Radius of Earth in km
		const lat1_rad = lat1 * Math.PI/180; 
		const lat2_rad = lat2 * Math.PI/180;
		const lat_delta = (lat2-lat1) * Math.PI/180;
		const lng_delta = (lon2-lon1) * Math.PI/180;

		const a = Math.sin(lat_delta/2) * Math.sin(lat_delta/2) +
		          Math.cos(lat1_rad) * Math.cos(lat2_rad) *
		          Math.sin(lng_delta/2) * Math.sin(lng_delta/2);
		const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

		const d = R * c; // in km

		// distance in km:
		return d;

	};


	var getBearing = function (lng1, lat1, lng2, lat2) {
		const lat1_rad = lat1 * Math.PI/180;
		const lng1_rad = lng1 * Math.PI/180;
		const lat2_rad = lat2 * Math.PI/180;
		const lng2_rad = lng2 * Math.PI/180;
		

		const y = Math.sin(lng2_rad-lng1_rad) * Math.cos(lat2_rad);
		const x = Math.cos(lat1_rad)*Math.sin(lat2_rad) - Math.sin(lat1_rad)*Math.cos(lat2_rad)*Math.cos(lng2_rad-lng1_rad);
		const theta = Math.atan2(y, x);
		const brng = (theta*180/Math.PI + 360) % 360; // in degrees

		return brng

	};

	var getBounds = function(longitude, latitude, radius){
		/* 
	
			helper function for mapboxgl.fitBounds().

			mapboxgl.fitBounds() takes two coordinate pairs as it's arguments.

			The first pair define the southwestern corner.
			The second pair define the northeastern corner.

			For this calculating the midpoint bewteen the boxes corners = the radius.
			
			radius units is expected to be in km.
		*/


		// left midpoint; bearing = 270:
		var left_midpoint = getEndpoint(latitude, longitude, 270, radius);
		// console.log("left_midpoint = " + left_midpoint);

		// right midpoint; bearing = 90:
		var right_midpoint = getEndpoint(latitude, longitude, 90, radius);
		// console.log("right_midpoint = " + right_midpoint);


		// upper midpoint; bearing = 0:
		var upper_midpoint = getEndpoint(latitude, longitude, 0, radius);
		// console.log("upper_midpoint = " + upper_midpoint);

		// lower midpoint; bearing = 180: 
		var lower_midpoint = getEndpoint(latitude, longitude, 180, radius);
		// console.log("lower_midpoint = " + lower_midpoint);

		southwestCorner = [right_midpoint[0], lower_midpoint[1]];
		northeastCorner = [left_midpoint[0], upper_midpoint[1]];

		return [southwestCorner, northeastCorner];

	};


	var buildLocationFeatures = function(locations) {

		var location_points = new Array;

		// build map points for each filtered location:
		locations.forEach(function(location){
			location_points.push({
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


		return location_points;
	};


	var updateMap = function(mapObj, locations) {
		mapObj.removeLayer('locations');
		mapObj.removeSource('locations');

		mapObj.addSource('locations', {
			'type': 'geojson',
			'data': {
				'type': 'FeatureCollection',
				'features': buildLocationFeatures(locations)
			}
		});

		mapObj.addLayer({
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


	var createMap = function(locations, longitude, latitude, distance, map_api_key) {

		// console.log("distance = " + distance);

		mapboxgl.accessToken = map_api_key;

		const map = new mapboxgl.Map({
			container: 'map-locations', // container ID
			style: 'mapbox://styles/mapbox/streets-v12', // style URL
			center: [longitude, latitude], // starting center in [lng, lat]
		});

		// sets the map view area. 2.6 is 2.6km and is the map display radius:
		// map.fitBounds(mapHelpers.getBounds(longitude, latitude, 2.6));
		map.fitBounds(getBounds(longitude, latitude, distance));

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
					'features': buildLocationFeatures(locations)
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

		return map;
		
	};





	return {
		createMap: createMap,
		updateMap: updateMap,
		getEndpoint: getEndpoint,
		getDistance: getDistance,
		getBearing: getBearing
	}

};




})();