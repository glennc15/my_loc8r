(function() {


angular
	.module('myLoc8rApp')
	.service('authentication', authentication);


authentication.$inject = ["$window", "$http"];
function authentication ($window, $http) {

	var register = function(user) {

		console.log('register user = ' + user);
		return $http.post('api/register', user)
					.success(
						function(data){
							console.log("success data: " + data);
							saveToken(data.token);
						});
	};

	var login = function(user) {
		return $http.post('api/login', user).success(function(data){saveToken(data.token);});
	};

	var logout = function() {
		console.log("logout()")
		$window.localStorage.removeItem('myLoc8r-token');
	};

	var saveToken = function(token) {
		$window.localStorage['myLoc8r-token'] = token;
	};

	var getToken = function() {
		return $window.localStorage['myLoc8r-token'];
	};

	var isLoggedIn = function() {
		var token = getToken();

		if (token) {
			var payload = JSON.parse($window.atob(token.split('.')[1]));

			return payload.exp > Date.now() / 1000;

		} else {
			return false;

		}
	
	};

	var currentUser = function() {
		if (isLoggedIn()) {
			var token = getToken();
			var payload = JSON.parse($window.atob(token.split('.')[1]));

			console.log(JSON.stringify(payload));

			return {
				email: payload.email,
				name: payload.name
			};
		}
	};


	return {
		saveToken: saveToken,
		getToken: getToken,
		register: register,
		login: login,
		logout: logout,
		isLoggedIn: isLoggedIn,
		currentUser: currentUser
	};



};





})();