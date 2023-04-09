(function (){


var locationsMapCtrl = function () {
	vm = this;


	// console.log($scope); 
	// console.log(vm); 

	// console.log(typeof $scope.locations);     

	console.log(locations);

	// $scope.locations.forEach(function(location){
	// 	console.log(location);

	// });

	// $scope.$apply(function() {

	// if ($scope.locations) {
	// 	console.log("locationsMapCtrl");
	// 	console.log($scope);
	// 	console.log($scope.locations);      
	// }

	// });



};



angular 
	.module('myLoc8rApp')
	.controller('locationsMapCtrl', locationsMapCtrl);

})();