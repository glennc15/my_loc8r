(function() {

var mapHelpers = function() {

	var degrees2radians = function(degrees) {
		return degrees * Math.PI/180;
	};



	var radians2degrees = function(radians) {
		return radians *  180 / Math.PI;
	};



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

	}

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



	return {
		getBounds: getBounds
	}

};


angular
	.module('myLoc8rApp')
	.service('mapHelpers', mapHelpers);



})();