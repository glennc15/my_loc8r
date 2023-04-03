angular.module('myApp', []);

var myController = function($scope) {
	$scope.myInput = "DICKHEAD!";
	$scope.test_val = "Test Value";

	$scope.data = [
		{
			name: "Title 1"
		},
		{
			name: 'Title 2'
		},
		{
			name: 'Title 3'
		},
	];


};


// angular
// 	.module('myApp')
// 	.controller('myController', myController);