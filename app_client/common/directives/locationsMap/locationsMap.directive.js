(function() {


var locationsMap = function() {
	return {
		restrict: 'EA',
		scope: {
			locations: '='
		},
		templateUrl: '/common/directives/locationsMap/locationsMap.template.html',
		controller: 'locationsMapCtrl as mapvm',
	};

};


angular 
	.module('myLoc8rApp')
	.directive('locationsMap', locationsMap);


})();