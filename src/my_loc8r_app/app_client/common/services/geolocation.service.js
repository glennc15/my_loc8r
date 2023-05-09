(function() {

angular
	.module('myLoc8rApp')
	.service('geolocation', geolocation);


function geolocation() {
	var getPosition = function(cbSuccess, cbError, cbNoGeo) {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(cbSuccess, cbError);

		}
		else {
			cbNoGeo();

		}
	
	};


	return {getPosition: getPosition};
};





// angular
// 	.module('myLoc8rApp')
// 	.service('geolocation', function() {
// 		var getPosition = function(cbSuccess, cbError, cbNoGeo) {
// 			if (navigator.geolocation) {
// 				navigator.geolocation.getCurrentPosition(cbSuccess, cbError);

// 			}
// 			else {
// 				cbNoGeo();

// 			}
		
// 		};


// 		return {getPosition: getPosition};
// });


})();