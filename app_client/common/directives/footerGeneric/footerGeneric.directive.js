(function() {
	
	var footerGeneric = function() {
		return {
			restrict: 'EA',
			templateUrl: '/common/directives/footerGeneric/footerGeneric.template.html'

		};
	};


angular
	.module('myLoc8rApp')
	.directive('footerGeneric', footerGeneric);



})();