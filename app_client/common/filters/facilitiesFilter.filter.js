(function() {

angular
	.module('myLoc8rApp')
	.filter('facilitiesFilter', facilitiesFilter);

function facilitiesFilter() {

	var filterLocations = function(locations, facility) {
		var filtered_locations = new Array;

		locations.forEach(function(location){
			if (location.facilities.includes(facility)) {
				filtered_locations.push(location);
			}

		})

		return filtered_locations;

	};	


	return function(locations, facilities){
		// console.log('facilitiesFilter yall!');
		// console.log("facilities = " + JSON.stringify(facilities));
		// console.log("locations = " + locations);

		if (Array.isArray(locations) && Array.isArray(facilities)) {
			if (facilities.length > 0){
				var filtered_locations = null;

				facilities.forEach(function(facility, idx, facilities_arr){
					
					if (idx == 0){
						filtered_locations = filterLocations(locations, facility);

					} else {
						filtered_locations = filterLocations(filtered_locations, facility);

					}
				});

				return filtered_locations;

			} else {
				return locations;

			}
			
		}
	};
};






})();