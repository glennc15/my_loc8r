(function() {

angular 
	.module('myLoc8rApp')
	.controller('addReviewCtrl', addReviewCtrl);

addReviewCtrl.$inject = ["$routeParams", "$location", "myLoc8rData", "authentication", "$window"];
function addReviewCtrl($routeParams, $location, myLoc8rData, authentication, $window) {
	var vm = this;
	vm.isLoggedIn = authentication.isLoggedIn()

	vm.currentPath = "/" + $routeParams.locationid + "?lng=" + $routeParams.lng + "&lat=" + $routeParams.lat + "&dist=" + $routeParams.dist;


	// initialize form data:
	vm.formData = {
		rating: 5,
		name: null,
		reviewText: null
	};


	vm.returnPage = $location.search().page || '/';


	vm.pageHeader = {
		title: "Add Review"
	};


	// 17 May 23: if we get here then the location is in session data so load
	// it and find the correct location:
	var locations = JSON.parse($window.sessionStorage['myLoc8r-locations']);
	let location = locations.find(t => t._id === $routeParams.locationid);
	vm.data = {location: location};


	// myLoc8rData.locationById($routeParams.locationid)
	// 	.success(function(location) {
	// 		vm.data = {location: location.data};

	// 	})
	// 	.error(function(e) {
	// 		console.log(e);

	// 	});


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
			vm.doAddReview($routeParams.locationid, vm.formData);

			return false;

		}

	};


	vm.gotoLocation = function() {
		$window.location.href = "/#location" + vm.currentPath;

	}


	vm.doAddReview = function(locationid, formData) {
		$window.sessionStorage.removeItem('myLoc8r-locations');


		myLoc8rData.addReviewById(locationid, {
				author: formData.name,
				rating: formData.rating,
				reviewText: formData.reviewText
			})
			.success(function(data) {
				// console.log("Form Submit success!");
				// console.log(data);
				vm.gotoLocation();

			})
			.error(function(data){
				vm.formError = "Your review has not been saved, try again!";
				// console.log("Form Submit Error!");
				// console.log(data);

			});


		return false;

	};




};


})();