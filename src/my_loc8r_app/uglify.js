var uglifyJs = require("uglify-js");
var fs = require('fs');


var appClientFilenames = [
	"app_client/app.js",
	"app_client/home/home.controller.js",
	"app_client/locations/locations.controller.js",
	"app_client/locationDetail/locationDetail.controller.js",
	"app_client/about/about.controller.js",
	"app_client/auth/register/register.controller.js",
	"app_client/auth/login/login.controller.js",
	"app_client/addReview/addReview.controller.js",
	"app_client/common/services/myLoc8rData.service.js",
	"app_client/common/services/geolocation.service.js",
	"app_client/common/services/authentication.service.js",
	"app_client/common/services/mapHelpers.service.js",
	"app_client/common/directives/ratingStars/ratingStars.directive.js",
	"app_client/common/directives/footerGeneric/footerGeneric.directive.js",
	"app_client/common/directives/navigation/navigation.directive.js",
	"app_client/common/directives/navigation/navigation.controller.js",
	"app_client/common/directives/pageHeader/pageHeader.directive.js",
	"app_client/common/directives/locationData/locationData.directive.js",
	"app_client/common/filters/formatDistance.filter.js",
	"app_client/common/filters/addHtmlLineBreaks.filter.js",
	"app_client/common/filters/isRating.filter.js",
	"app_client/common/filters/isOpenNow.filter.js",
	"app_client/common/filters/facilitiesFilter.filter.js",
];

var appClientFiles = new Array;

appClientFilenames.forEach(function(filename) {
	appClientFiles.push(fs.readFileSync(filename, 'utf8'));

});


var uglified = uglifyJs.minify(appClientFiles, {compress: false});

// console.log("uglified: " + uglified.code);

fs.writeFile('app_client/lib/angular/myLoc8r.min.js', uglified.code, function(err) {
	if (err) {
		console.log("Error building: myLoc8r.min.js");
		console.log(err);

	} else {
		console.log("Script generated and saved: myLoc8r.min.js");

	}


});