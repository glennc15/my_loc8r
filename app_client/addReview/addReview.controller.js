(function() {


var addReviewCtrl = function($routeParams, myLoc8rData, authentication, $window) {
	var vm = this;
	vm.isLoggedIn = authentication.isLoggedIn()

	vm.currentPath = "/" + $routeParams.locationid + "?lng=" + $routeParams.lng + "&lat=" + $routeParams.lat + "&dist=" + $routeParams.dist;


	// initialize form data:
	vm.formData = {
		rating: 5,
		name: null,
		reviewText: null
	};




	vm.pageHeader = {
		title: "Add Review"
	};

	myLoc8rData.locationById($routeParams.locationid)
		.success(function(location) {

			vm.data = {location: location.data};

	


		})
		.error(function(e) {
			console.log(e);

		});



	vm.onSubmit = function() {
		vm.formError = "";

		// if (!vm.formData.name || !vm.formData.rating || !vm.formData.reviewText) {
		if (!vm.formData.rating || !vm.formData.reviewText) {

			vm.formError = "All fields required, please try again";

			// console.log('vm.formError: ' + vm.formError);
			// console.log('authentication.currentUser = ' + JSON.stringify(authentication.currentUser()));

			return false;

		} else{
			// add the user's name and submit:
			vm.formData.name = authentication.currentUser().name;

			// console.log(JSON.stringify(vm.formData));
			vm.doAddReview($routeParams.locationid, vm.formData);
			vm.gotoLocation();

			return false;

		}

	};


	vm.gotoLocation = function() {
		$window.location.href = "/location" + vm.currentPath;
	}




	vm.doAddReview = function(locationid, formData) {

		myLoc8rData.addReviewById(locationid, {
				author: formData.name,
				rating: formData.rating,
				reviewText: formData.reviewText
			})
			.success(function(data) {
				console.log("Form Submit success!");
				console.log(data);
				// vm.modal.close(data);

			})
			.error(function(data){
				vm.formError = "Your review has not been saved, try again!";
				console.log("Form Submit Error!");
				console.log(data);

			});

		return false;

	};




};



angular 
	.module('myLoc8rApp')
	.controller('addReviewCtrl', addReviewCtrl);

})();