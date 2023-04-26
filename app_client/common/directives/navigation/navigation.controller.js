(function() {


var navigationCtrl = function($location, authentication) {
	var vm = this;

	vm.currentPath = $location.path();

	// console.log("$location.path(): "  + $location.path());

	vm.isLoggedIn = authentication.isLoggedIn();

	vm.currentUser = authentication.currentUser();

	vm.logout = function() {

		authentication.logout();
		$location.path('/');

		vm.isLoggedIn = authentication.isLoggedIn();

	};
};



angular
	.module('myLoc8rApp')
	.controller('navigationCtrl', navigationCtrl);


})();

