(function() {

var locationData = function() {

	return {
		restrict: "EA",
		scope: {
			location: "=location"
		},
		templateUrl: '/common/directives/locationData/locationData.template.html'
	};



};


angular
	.module('myLoc8rApp')
	.directive('locationData', locationData);




})();