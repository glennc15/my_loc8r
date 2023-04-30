(function() {


angular
	.module('myLoc8rApp')
	.filter('formatDistance', formatDistance);

function formatDistance() {
	var _isNumeric = function (n) {
		return !isNaN(parseFloat(n)) && isFinite(n);
	};


	return function (distance) {
		var numDistance, unit;
		
		if (distance && _isNumeric(distance)){		
			if (distance > 1) {
				numDistance = parseFloat(distance).toFixed(1);
				unit = 'km';
			
			} else{
				numDistance = parseInt(distance * 1000, 10);
				unit = 'm';
			}

			return numDistance + unit;

		} else {
			return "?";
		
		}

	};
};


})();