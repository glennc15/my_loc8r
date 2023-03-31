(function(){
	
	var navigation =function () {
		return {
			restrict: 'EA',
			templateUrl: '/common/directives/navigation/navigation.template.html',
			controller: 'navigationCtrl as navvm'
		};
	};


angular
	.module('myLoc8rApp')
	.directive('navigation', navigation);


})();