(function() {

angular
	.module('myLoc8rApp')
	.directive('locationData', locationData);


function locationData() {

	return {
		restrict: "EA",
		scope: {
			location: "=location",
			currentLat: '=',
			currentLng: '=',
		},
		templateUrl: '/common/directives/locationData/locationData.template.html'
	};

};


})();