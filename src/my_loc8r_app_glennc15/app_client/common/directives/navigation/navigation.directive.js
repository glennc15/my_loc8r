(function(){

angular
	.module('myLoc8rApp')
	.directive('navigation', navigation);
	
function navigation() {
	return {
		restrict: 'EA',
		templateUrl: '/common/directives/navigation/navigation.template.html',
		controller: 'navigationCtrl as navvm'
	};
};


})();