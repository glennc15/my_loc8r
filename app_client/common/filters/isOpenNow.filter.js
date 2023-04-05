(function() {

var weekday2Number = function(weekday) {
	var weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

	var dayOfWeek = weekDays.findIndex(function(x) {
		return (x == weekday);
	}) + 1;


	return dayOfWeek;
}

var timestr2date = function(time_str) {
	var hours = parseInt(time_str.split(':')[0])
	var minutes = parseInt(time_str.split(':')[1].slice(0,2));

	if (time_str.includes('pm')) {
		hours += 12;
	}

	var this_date = new Date();

	this_date.setHours(hours);
	this_date.setMinutes(minutes);
	this_date.setSeconds(0);
	this_date.setMilliseconds(0);

	return this_date;

};

var isOpenNow = function() {
	return function(openingTimes){

		var is_open_now = false;


		// find the openingTime that matches the current day of the week
		var openingTimeFound = false;
		var current_time = new Date();



		openingTimes.forEach(function(openingTime) {

			// use this when .days is a range of weekdays:
			if (openingTime.days.includes(' - ')) {
				var start_day = weekday2Number(openingTime.days.split(' - ')[0]);
				var end_day = weekday2Number(openingTime.days.split(' - ')[1]);



				if ((start_day <= current_time.getDay()) && (current_time.getDay() <= end_day)) {
					openingTimeFound = true;
				}

			// .days is a single weekday:
			} else {
				if (weekday2Number(openingTime.days) == current_time.getDay()) {
					openingTimeFound = true;

				}
			}

			// an opening time object was found for the current day. Now check
			// if the current time is within the operating hours for today:
			if (openingTimeFound) {

				// ensure the location is open on the current weekday:
				if (!openingTime.closed) {
					// console.log("Today: " + current_time);
					// console.log("Matching openingTime: " + JSON.stringify(openingTime));

					var open_time = timestr2date(openingTime.opening);
					var close_time = timestr2date(openingTime.closing);

					if ((open_time <= current_time) && (current_time <= close_time)){
						// console.log("current_time: " + current_time);
						// console.log("open_time: " + open_time);
						// console.log("close_time: " + close_time);
						// console.log(JSON.stringify(openingTime));

						is_open_now = true;
					} 
				}
			}
		});

		return is_open_now;
	};
};


// var isOpenNow = function() {
// 	return function(openingTimes) {
// 		console.log("openingTimes = " + JSON.stringify(openingTimes));
// 	};
// };


angular 
	.module('myLoc8rApp')
	.filter('isOpenNow', isOpenNow);


})();


