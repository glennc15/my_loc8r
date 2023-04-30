(function() {


angular
	.module('myLoc8rApp')
	.filter('isRating', isRating);
	
function isRating() {
	return function(rating) {

		if (!isNaN(rating)) {

			var rating_int = parseInt(rating);

			if (rating_int >= 1 && rating_int <=5) {
				return true;
			} else {
				return false;

			};

		} else {
			return false;
		};


	};
};


})();