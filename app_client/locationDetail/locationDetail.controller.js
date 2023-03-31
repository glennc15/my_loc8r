(function() {

var locationDetailCtrl = function($routeParams, myLoc8rData, $modal, $location, authentication) {
	var vm = this;

	vm.locationid = $routeParams.locationid;

	vm.isLoggedIn = authentication.isLoggedIn();

	vm.currentPath = $location.path();

	vm.pageHeader = {
		title: "Location detail page"
	};


	myLoc8rData.locationById($routeParams.locationid)
		.success(function(location) {

			// facilities come from the api as a string with each facility
			// seperated by a ',', the view expects facilities to be an
			// array of strings. So converting facilties to the correct format.
			location['facilities'] = location['facilities'].split(',');

			vm.data = {location: location};
			
			vm.pageHeader = {
				title: vm.data.location.name
			};


		})
		.error(function(e) {
			console.log(e);

		});


		vm.popupReviewForm = function() {
			var modalInstance = $modal.open({
				templateUrl: '/reviewModal/reviewModal.view.html',
				controller: 'reviewModalCtrl as vm',
				resolve: {
					locationData: function() {
						return {
							locationid: vm.locationid,
							locationName: vm.data.location.name
						};
					}
				}
			});


			modalInstance.result.then(function(data){
				vm.data.location.reviews.push(data);
				
			});
		};





};


angular
	.module('myLoc8rApp')
	.controller('locationDetailCtrl', locationDetailCtrl);

})();






