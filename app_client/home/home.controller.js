(function() {


// function homeCtrl ($scope, $filter, myLoc8rData, geolocation, mapHelpers, testData) {
function homeCtrl ($scope, $filter, myLoc8rData, geolocation, mapHelpers) {
	var vm = this;

	vm.pageHeader = {
		title: 'myLoc8r',
		strapline: "Find places to work with wifi near you!",
		content: "Looking for wifi and a seat? We help you find places to work when out and about. Perhaps with coffee, cake or a pint? Let myLoc8r help you find the place you're looking for."

	};

};


angular
	.module('myLoc8rApp')
	.controller('homeCtrl', homeCtrl);

})();