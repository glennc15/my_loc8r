(function() {

var locationData = function() {

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


angular
	.module('myLoc8rApp')
	.directive('locationData', locationData);




})();