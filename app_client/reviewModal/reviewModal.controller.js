(function() {

var reviewModalCtrl = function ($modalInstance, myLoc8rData, locationData) {
	var vm = this;
	vm.locationData = locationData;


	// initialize form data:
	vm.formData = {
		rating: 5,
		name: null,
		reviewText: null
	};

	// vm.formData = {
	// 	rating: 3,
	// 	name: "Carl",
	// 	reviewText: "My mediocre review."
	// };



	vm.onSubmit = function() {
		vm.formError = "";

		// if (!vm.formData.name || !vm.formData.rating || !vm.formData.reviewText) {
		if (!vm.formData.rating || !vm.formData.reviewText) {

			vm.formError = "All fields required, please try again";

			return false;

		} else{
			vm.doAddReview(vm.locationData.locationid, vm.formData);

			return false;

		}

	};


	vm.doAddReview = function(locationid, formData) {

		myLoc8rData.addReviewById(locationid, {
				author: formData.name,
				rating: formData.rating,
				reviewText: formData.reviewText
			})
			.success(function(data) {
				console.log("Form Submit success!");
				console.log(data);
				vm.modal.close(data);

			})
			.error(function(data){
				vm.formError = "Your review has not been saved, try again!";
				console.log("Form Submit Error!");
				console.log(data);

			});

		return false;

	};


	vm.modal = {
		close: function(result) {
			$modalInstance.close(result);
		},

		cancel: function() {
			$modalInstance.dismiss('cancel');
		}
	};

};

angular
	.module('myLoc8rApp')
	.controller('reviewModalCtrl', reviewModalCtrl);

})();