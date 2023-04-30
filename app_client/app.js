(function() {


// angular.module('myLoc8rApp', ['ngRoute', 'ngSanitize', 'ui.bootstrap']);
angular.module('myLoc8rApp', ['ngRoute', 'ngSanitize']);




function config ($routeProvider, $locationProvider) {
	
	$routeProvider
		.when('/', {
			templateUrl: 'home/home.view.html',
			controller: 'homeCtrl',
			controllerAs: 'vm'
		})
		.when('/locations', {
			templateUrl: 'locations/locations.view.html',
			controller: 'locationsCtrl',
			controllerAs: 'vm'
		})
		.when('/about', {
			// templateUrl: '/common/views/genericText.view.html',
			templateUrl: '/about/about.view.html',
			controller: 'aboutCtrl',
			controllerAs: 'vm'
		})
		.when('/location/:locationid', {
			templateUrl: '/locationDetail/locationDetail.view.html',
			controller: 'locationDetailCtrl',
			controllerAs: 'vm'
		})
		.when('/addreview/:locationid', {
			templateUrl: '/addReview/addReview.view.html',
			controller: 'addReviewCtrl',
			controllerAs: 'vm'
		})
		.when('/register', {
			templateUrl: '/auth/register/register.view.html',
			controller: 'registerCtrl',
			controllerAs: 'vm'
		})
		.when('/login', {
			templateUrl: '/auth/login/login.view.html',
			controller: 'loginCtrl',
			controllerAs: 'vm'
		})
		.otherwise({redirectTo: '/'});

	$locationProvider.html5Mode(true);

};


angular
	.module('myLoc8rApp')
	.config(['$routeProvider', '$locationProvider', config]);


})();
