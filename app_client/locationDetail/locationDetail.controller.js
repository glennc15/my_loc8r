(function() {

// var locationDetailCtrl = function($routeParams, myLoc8rData, $modal, $location, authentication, mapHelpers) {
var locationDetailCtrl = function($routeParams, myLoc8rData, $location, authentication, mapHelpers) {

	var vm = this;

	vm.locationid = $routeParams.locationid;

	vm.isLoggedIn = authentication.isLoggedIn();

	vm.currentPath = "/" + $routeParams.locationid + "?lng=" + $routeParams.lng + "&lat=" + $routeParams.lat + "&dist=" + $routeParams.dist;



	myLoc8rData.locationById($routeParams.locationid)
		.success(function(location) {

			// facilities come from the api as a string with each facility
			// seperated by a ',', the view expects facilities to be an
			// array of strings. So converting facilties to the correct format.
			location.data['facilities'] = location.data['facilities'].split(',');

			vm.data = {location: location.data};

			// author short name: [first name] [first initial in last name]
			vm.data.location.reviews.forEach(function(review) {
				review.authorShort = review.author.split(' ')[0] + ' ' + review.author.split(' ')[1][0];
				review.moment = moment(review.created_on).fromNow();

			});
			
			vm.pageHeader = {
				title: vm.data.location.name
			};

			var mapWindow = Math.ceil($routeParams.dist*10)/10;
			vm.map = mapHelpers.createMap([vm.data.location], $routeParams.lng, $routeParams.lat, mapWindow, location.map_key);

		})
		.error(function(e) {
			console.log(e);

		});


};


angular
	.module('myLoc8rApp')
	.controller('locationDetailCtrl', locationDetailCtrl);

})();






