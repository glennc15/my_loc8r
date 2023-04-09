(function() {


var testData = function() {

	var location = function(){
		var location = {location: 'location data'};

		return location;

	};


	var locations = function(){
		var these_locations = [
		  {
		    "_id": "6425e437e0dd8621c2ab27e7",
		    "address": " 7890 Magnolia Street",
		    "dist_calc": 0.044485946212170696,
		    "facilities": "Music Ambiance,Power Outlets",
		    "lat": 12.916074159702077,
		    "lng": 100.86141302625707,
		    "name": "The Steaming Mug ",
		    "openingTimes": [
		      {
		        "_id": "6425e437e0dd8621c2ab27e4",
		        "closed": false,
		        "closing": "6:00pm",
		        "days": "Monday - Friday",
		        "opening": "8:00am"
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27e5",
		        "closed": true,
		        "days": "Saturday"
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27e6",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 2,
		    "reviews": [
		      {
		        "_id": "6425e437e0dd8621c2ab27e9",
		        "author": "Chaney Logan",
		        "author_id": "6425e433e0dd8621c2ab2740",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 2,
		        "review_text": "The coffee shop had a nice ambiance, and while the wifi wasn't the fastest, it was enough to get some work done."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab27eb",
		        "author": "Malcolm Mclean",
		        "author_id": "6425e431e0dd8621c2ab26e9",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is some of the fastest I've ever experienced, and the coffee is delicious. It's the perfect place to work or study."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab27ed",
		        "author": "Vernon Nielsen",
		        "author_id": "6425e432e0dd8621c2ab26f9",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab27ef",
		        "author": "Shaeleigh Padilla",
		        "author_id": "6425e431e0dd8621c2ab26db",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop was decent, but not the fastest. However, the comfortable seating and delicious coffee made up for it."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab27f1",
		        "author": "Magee Mason",
		        "author_id": "6425e437e0dd8621c2ab27c7",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop has amazing coffee and great wifi. I was able to get a lot of work done in a comfortable and cozy atmosphere."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab27f3",
		        "author": "Candice Knowles",
		        "author_id": "6425e434e0dd8621c2ab276d",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop could be better, but the coffee was great and the staff was friendly and attentive."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab27f5",
		        "author": "Cynthia Fowler",
		        "author_id": "6425e438e0dd8621c2ab27f4",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 2,
		        "review_text": "The coffee at this shop was good, but the wifi was a bit slow. Still, it was a nice place to relax and catch up on some work."
		      }
		    ],
		    "views": 20
		  },
		  {
		    "_id": "6425e43be0dd8621c2ab286d",
		    "address": " 6789 Pinecone Avenue",
		    "dist_calc": 0.6964628745975018,
		    "facilities": "Espresso Machines,Outdoor Seating,Specialty Drinks,Music Ambiance",
		    "lat": 12.921940459113447,
		    "lng": 100.86154019966963,
		    "name": "Cafe Mocha ",
		    "openingTimes": [
		      {
		        "_id": "6425e43be0dd8621c2ab286c",
		        "closed": false,
		        "closing": "5:00pm",
		        "days": "Monday - Sunday",
		        "opening": "9:00am"
		      }
		    ],
		    "rating": 4,
		    "reviews": [
		      {
		        "_id": "6425e43be0dd8621c2ab286f",
		        "author": "Demetria Harvey",
		        "author_id": "6425e431e0dd8621c2ab26ca",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 5,
		        "review_text": "The coffee at this shop is consistently good, and the wifi is fast and reliable. It's the perfect spot to get some work done while enjoying a great cup of coffee."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2871",
		        "author": "Magee Mason",
		        "author_id": "6425e437e0dd8621c2ab27c7",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2873",
		        "author": "Bianca Salas",
		        "author_id": "6425e431e0dd8621c2ab26d5",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 2,
		        "review_text": "The coffee at this shop was good, but the wifi was a bit slow. Still, it was a nice place to relax and catch up on some work."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2875",
		        "author": "Alea Cannon",
		        "author_id": "6425e43ae0dd8621c2ab2857",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop has amazing coffee and great wifi. I was able to get a lot of work done in a comfortable and cozy atmosphere."
		      }
		    ],
		    "views": 6
		  },
		  {
		    "_id": "6425e433e0dd8621c2ab272e",
		    "address": " 1234 Cherry Street",
		    "dist_calc": 1.1043924787759534,
		    "facilities": "Specialty Drinks",
		    "lat": 12.9255769995059,
		    "lng": 100.86226754210986,
		    "name": "The Grind House ",
		    "openingTimes": [
		      {
		        "_id": "6425e433e0dd8621c2ab272d",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": "Monday - Sunday",
		        "opening": "7:00am"
		      }
		    ],
		    "rating": 3,
		    "reviews": [
		      {
		        "_id": "6425e433e0dd8621c2ab2730",
		        "author": "Ashton Bright",
		        "author_id": "6425e432e0dd8621c2ab2707",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop could be better, but the coffee was great and the staff was friendly and attentive."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2732",
		        "author": "Constance Glenn",
		        "author_id": "6425e433e0dd8621c2ab2731",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 1,
		        "review_text": "I was really looking forward to trying this coffee shop, but the wifi was so slow that I couldn't even load a webpage."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2734",
		        "author": "Chancellor Livingston",
		        "author_id": "6425e433e0dd8621c2ab2733",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop is my go-to spot for delicious coffee and fast wifi. The staff is friendly and the atmosphere is relaxing."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2736",
		        "author": "Mufutau Conway",
		        "author_id": "6425e431e0dd8621c2ab26f1",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 5,
		        "review_text": "The coffee at this shop was excellent, and the fast wifi made it easy for me to stay connected while I worked."
		      }
		    ],
		    "views": 5
		  },
		  {
		    "_id": "6425e431e0dd8621c2ab26d4",
		    "address": " 5678 Elm Street",
		    "dist_calc": 1.2118945955570761,
		    "facilities": "Seating Options,Tea Selection,Music Ambiance,To-go Cups",
		    "lat": 12.926557961462876,
		    "lng": 100.86204443749396,
		    "name": "Brew House Caf\u00e9 ",
		    "openingTimes": [
		      {
		        "_id": "6425e431e0dd8621c2ab26d0",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": "Monday - Thursday",
		        "opening": "6:30am"
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26d1",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": " Friday",
		        "opening": "6:30am"
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26d2",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": " Saturday",
		        "opening": "7:30am"
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26d3",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": " Sunday",
		        "opening": "7:30am"
		      }
		    ],
		    "rating": 4,
		    "reviews": [
		      {
		        "_id": "6425e431e0dd8621c2ab26d6",
		        "author": "Bianca Salas",
		        "author_id": "6425e431e0dd8621c2ab26d5",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 2,
		        "review_text": "The wifi was a bit spotty, but the coffee was delicious and the seating was comfortable. It's a great place to relax and read a book."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26d8",
		        "author": "Harding Maddox",
		        "author_id": "6425e431e0dd8621c2ab26d7",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 5,
		        "review_text": "The coffee at this shop is consistently good, and the wifi is fast and reliable. It's the perfect spot to get some work done while enjoying a great cup of coffee."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26da",
		        "author": "Burton Gregory",
		        "author_id": "6425e431e0dd8621c2ab26d9",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26dc",
		        "author": "Shaeleigh Padilla",
		        "author_id": "6425e431e0dd8621c2ab26db",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is some of the fastest I've ever experienced, and the coffee is delicious. It's the perfect place to work or study."
		      }
		    ],
		    "views": 5
		  },
		  {
		    "_id": "6425e434e0dd8621c2ab2762",
		    "address": " 7890 Pineapple Street",
		    "dist_calc": 1.2187952137911726,
		    "facilities": "Outdoor Seating,Seating Options",
		    "lat": 12.926632775857595,
		    "lng": 100.86151837033617,
		    "name": "Bean Counter ",
		    "openingTimes": [
		      {
		        "_id": "6425e434e0dd8621c2ab2760",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": "Monday - Saturday",
		        "opening": "6:00am"
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab2761",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 4,
		    "reviews": [
		      {
		        "_id": "6425e434e0dd8621c2ab2764",
		        "author": "Bianca Salas",
		        "author_id": "6425e431e0dd8621c2ab26d5",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 3,
		        "review_text": "The coffee at this shop was good, but the wifi was a bit slow. Still, it was a nice place to relax and catch up on some work."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab2766",
		        "author": "Zena Rasmussen",
		        "author_id": "6425e433e0dd8621c2ab274b",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop has a great selection of coffee and pastries, and the fast wifi makes it a great spot to catch up on emails or work."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab2768",
		        "author": "Ingrid O'brien",
		        "author_id": "6425e432e0dd8621c2ab270d",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is some of the fastest I've ever experienced, and the coffee is delicious. It's the perfect place to work or study."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab276a",
		        "author": "Ruth Solis",
		        "author_id": "6425e431e0dd8621c2ab26f7",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab276c",
		        "author": "Clare Washington",
		        "author_id": "6425e433e0dd8621c2ab273c",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop is my go-to spot for delicious coffee and fast wifi. The staff is friendly and the atmosphere is relaxing."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab276e",
		        "author": "Candice Knowles",
		        "author_id": "6425e434e0dd8621c2ab276d",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 3,
		        "review_text": "The wifi was a bit spotty, but the coffee was delicious and the seating was comfortable. It's a great place to relax and read a book."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab2770",
		        "author": "Shaeleigh Padilla",
		        "author_id": "6425e431e0dd8621c2ab26db",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 5,
		        "review_text": "The coffee is amazing and the wifi is fast and reliable. This coffee shop has become my new favorite spot for a quick work session."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab2772",
		        "author": "Cyrus Whitfield",
		        "author_id": "6425e433e0dd8621c2ab272b",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab2774",
		        "author": "Vernon Nielsen",
		        "author_id": "6425e432e0dd8621c2ab26f9",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but the seating could be more comfortable. Overall, it's a nice spot to grab a cup of coffee and get some work done."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab2776",
		        "author": "Colt Reed",
		        "author_id": "6425e434e0dd8621c2ab2775",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 5,
		        "review_text": "The coffee at this shop was excellent, and the fast wifi made it easy for me to stay connected while I worked."
		      }
		    ],
		    "views": 11
		  },
		  {
		    "_id": "6425e432e0dd8621c2ab26fe",
		    "address": " 7890 Walnut Street",
		    "dist_calc": 1.2865377458152052,
		    "facilities": "Espresso Machines,Seating Options,Music Ambiance,Baked Goods",
		    "lat": 12.927230286122251,
		    "lng": 100.86202050120873,
		    "name": "Daily Grind Coffee Co. ",
		    "openingTimes": [
		      {
		        "_id": "6425e432e0dd8621c2ab26fd",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": "Monday - Sunday",
		        "opening": "7:00am"
		      }
		    ],
		    "rating": 4,
		    "reviews": [
		      {
		        "_id": "6425e432e0dd8621c2ab2700",
		        "author": "Hoyt Richardson",
		        "author_id": "6425e431e0dd8621c2ab26ef",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 4,
		        "review_text": "The coffee at this shop was excellent, and the fast wifi made it easy for me to stay connected while I worked."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab2702",
		        "author": "Mufutau Conway",
		        "author_id": "6425e431e0dd8621c2ab26f1",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 5,
		        "review_text": "The coffee at this shop is consistently good, and the wifi is fast and reliable. It's the perfect spot to get some work done while enjoying a great cup of coffee."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab2704",
		        "author": "Demetria Harvey",
		        "author_id": "6425e431e0dd8621c2ab26ca",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop has amazing coffee and great wifi. I was able to get a lot of work done in a comfortable and cozy atmosphere."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab2706",
		        "author": "Cameran Stuart",
		        "author_id": "6425e431e0dd8621c2ab26cc",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop is my go-to spot for delicious coffee and fast wifi. The staff is friendly and the atmosphere is relaxing."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab2708",
		        "author": "Ashton Bright",
		        "author_id": "6425e432e0dd8621c2ab2707",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is excellent, and the coffee is consistently good. It's the perfect spot to catch up on some work."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab270a",
		        "author": "Kameko Mejia",
		        "author_id": "6425e432e0dd8621c2ab2709",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is some of the fastest I've ever experienced, and the coffee is delicious. It's the perfect place to work or study."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab270c",
		        "author": "Wyatt Stephens",
		        "author_id": "6425e432e0dd8621c2ab270b",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab270e",
		        "author": "Ingrid O'brien",
		        "author_id": "6425e432e0dd8621c2ab270d",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab2710",
		        "author": "Vernon Nielsen",
		        "author_id": "6425e432e0dd8621c2ab26f9",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop has a great selection of coffee and pastries, and the fast wifi makes it a great spot to catch up on emails or work."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab2712",
		        "author": "Harding Maddox",
		        "author_id": "6425e431e0dd8621c2ab26d7",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 4,
		        "review_text": "The coffee is amazing and the wifi is fast and reliable. This coffee shop has become my new favorite spot for a quick work session."
		      }
		    ],
		    "views": 11
		  },
		  {
		    "_id": "6425e437e0dd8621c2ab27d5",
		    "address": " 3456 Laurel Street",
		    "dist_calc": 1.3655828920092816,
		    "facilities": "Outdoor Seating",
		    "lat": 12.927934222574502,
		    "lng": 100.86216823217879,
		    "name": "The Beanery ",
		    "openingTimes": [
		      {
		        "_id": "6425e437e0dd8621c2ab27d3",
		        "closed": false,
		        "closing": "8:00pm",
		        "days": "Monday - Saturday",
		        "opening": "7:00am"
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27d4",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e437e0dd8621c2ab27d7",
		        "author": "Shaeleigh Padilla",
		        "author_id": "6425e431e0dd8621c2ab26db",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 3,
		        "review_text": "The coffee at this shop was good, but the wifi was a bit slow. Still, it was a nice place to relax and catch up on some work."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27d9",
		        "author": "Constance Glenn",
		        "author_id": "6425e433e0dd8621c2ab2731",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 1,
		        "review_text": "I was really looking forward to trying this coffee shop, but the wifi was so slow that I couldn't even load a webpage."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27db",
		        "author": "Chase Sharp",
		        "author_id": "6425e435e0dd8621c2ab2785",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop could be better, but the coffee was great and the staff was friendly and attentive."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27dd",
		        "author": "McKenzie Steele",
		        "author_id": "6425e436e0dd8621c2ab27bb",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 1,
		        "review_text": "I would not recommend this coffee shop for anyone who needs to get work done. The wifi was virtually unusable."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27df",
		        "author": "Eleanor Soto",
		        "author_id": "6425e437e0dd8621c2ab27de",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 1,
		        "review_text": "The coffee was overpriced and the wifi was practically non-existent. I won't be coming back to this coffee shop."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27e1",
		        "author": "Astra Mckinney",
		        "author_id": "6425e432e0dd8621c2ab2721",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 2,
		        "review_text": "This coffee shop has a nice selection of coffee and pastries, and the wifi was decent enough for me to check my emails."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27e3",
		        "author": "Clare Washington",
		        "author_id": "6425e433e0dd8621c2ab273c",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      }
		    ],
		    "views": 7
		  },
		  {
		    "_id": "6425e439e0dd8621c2ab281a",
		    "address": " 1234 Park Street",
		    "dist_calc": 1.4793706530569843,
		    "facilities": "Restrooms,Coffee Machines,Restrooms,Espresso Machines",
		    "lat": 12.928971353043396,
		    "lng": 100.86175234896547,
		    "name": "Espresso Lane ",
		    "openingTimes": [
		      {
		        "_id": "6425e439e0dd8621c2ab2817",
		        "closed": false,
		        "closing": "6:00pm",
		        "days": "Monday - Friday",
		        "opening": "8:00am"
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab2818",
		        "closed": true,
		        "days": "Saturday"
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab2819",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 2,
		    "reviews": [
		      {
		        "_id": "6425e439e0dd8621c2ab281c",
		        "author": "Constance Glenn",
		        "author_id": "6425e433e0dd8621c2ab2731",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 1,
		        "review_text": "I would not recommend this coffee shop for anyone who needs to get work done. The wifi was virtually unusable."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab281e",
		        "author": "Ann Wood",
		        "author_id": "6425e432e0dd8621c2ab271b",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 1,
		        "review_text": "The coffee was nothing special, and the wifi was so slow that I couldn't even upload a simple document."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab2820",
		        "author": "Willow Chan",
		        "author_id": "6425e439e0dd8621c2ab281f",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 2,
		        "review_text": "The coffee at this shop was good, but the wifi was a bit slow. Still, it was a nice place to relax and catch up on some work."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab2822",
		        "author": "Winifred Cote",
		        "author_id": "6425e434e0dd8621c2ab275e",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop has a great selection of coffee and pastries, and the fast wifi makes it a great spot to catch up on emails or work."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab2824",
		        "author": "Robin Little",
		        "author_id": "6425e432e0dd8621c2ab26fb",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab2826",
		        "author": "Ruth Solis",
		        "author_id": "6425e431e0dd8621c2ab26f7",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to use my phone as a hotspot just to get some work done."
		      }
		    ],
		    "views": 6
		  },
		  {
		    "_id": "6425e438e0dd8621c2ab27fa",
		    "address": " 2345 Vine Street",
		    "dist_calc": 1.6674836054943876,
		    "facilities": "Music Ambiance,Baked Goods,Menu Displays",
		    "lat": 12.930649548594404,
		    "lng": 100.86216408867617,
		    "name": "The Coffee Coop ",
		    "openingTimes": [
		      {
		        "_id": "6425e438e0dd8621c2ab27f6",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": "Monday - Thursday",
		        "opening": "6:30am"
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab27f7",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": " Friday",
		        "opening": "6:30am"
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab27f8",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": " Saturday",
		        "opening": "7:30am"
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab27f9",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": " Sunday",
		        "opening": "7:30am"
		      }
		    ],
		    "rating": 4,
		    "reviews": [
		      {
		        "_id": "6425e438e0dd8621c2ab27fc",
		        "author": "Cameron Hart",
		        "author_id": "6425e431e0dd8621c2ab26ce",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab27fe",
		        "author": "Robin Little",
		        "author_id": "6425e432e0dd8621c2ab26fb",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop was fast and reliable, which made it the perfect spot for a quick coffee break and some work."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab2800",
		        "author": "Harding Maddox",
		        "author_id": "6425e431e0dd8621c2ab26d7",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop has amazing coffee and great wifi. I was able to get a lot of work done in a comfortable and cozy atmosphere."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab2802",
		        "author": "Harrison Howe",
		        "author_id": "6425e435e0dd8621c2ab2781",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 5,
		        "review_text": "The coffee is amazing and the wifi is fast and reliable. This coffee shop has become my new favorite spot for a quick work session."
		      }
		    ],
		    "views": 6
		  },
		  {
		    "_id": "6425e43fe0dd8621c2ab290c",
		    "address": " 7890 Elmwood Avenue",
		    "dist_calc": 1.7089204714513564,
		    "facilities": "Espresso Machines",
		    "lat": 12.930964348150646,
		    "lng": 100.86301882837654,
		    "name": "The Coffee Commune ",
		    "openingTimes": [
		      {
		        "_id": "6425e43fe0dd8621c2ab290b",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": "Monday - Sunday",
		        "opening": "7:00am"
		      }
		    ],
		    "rating": 3,
		    "reviews": [
		      {
		        "_id": "6425e43fe0dd8621c2ab290e",
		        "author": "Kameko Mejia",
		        "author_id": "6425e432e0dd8621c2ab2709",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab2910",
		        "author": "Shaeleigh Padilla",
		        "author_id": "6425e431e0dd8621c2ab26db",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop is my go-to spot for delicious coffee and fast wifi. The staff is friendly and the atmosphere is relaxing."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab2912",
		        "author": "Colt Reed",
		        "author_id": "6425e434e0dd8621c2ab2775",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab2914",
		        "author": "Chase Sharp",
		        "author_id": "6425e435e0dd8621c2ab2785",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 4,
		        "review_text": "The coffee is amazing and the wifi is fast and reliable. This coffee shop has become my new favorite spot for a quick work session."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab2916",
		        "author": "Eleanor Soto",
		        "author_id": "6425e437e0dd8621c2ab27de",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 4,
		        "review_text": "The coffee at this shop is consistently good, and the wifi is fast and reliable. It's the perfect spot to get some work done while enjoying a great cup of coffee."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab2918",
		        "author": "Cynthia Fowler",
		        "author_id": "6425e438e0dd8621c2ab27f4",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 3,
		        "review_text": "The wifi at this coffee shop was decent, but not the fastest. However, the comfortable seating and delicious coffee made up for it."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab291a",
		        "author": "Cameran Stuart",
		        "author_id": "6425e431e0dd8621c2ab26cc",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is some of the fastest I've ever experienced, and the coffee is delicious. It's the perfect place to work or study."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab291c",
		        "author": "Jasmine Cabrera",
		        "author_id": "6425e431e0dd8621c2ab26e3",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 3,
		        "review_text": "The coffee shop had a nice ambiance, and while the wifi wasn't the fastest, it was enough to get some work done."
		      }
		    ],
		    "views": 8
		  },
		  {
		    "_id": "6425e43ae0dd8621c2ab283c",
		    "address": " 3456 Pinecone Street",
		    "dist_calc": 1.7609273548498001,
		    "facilities": "Outdoor Seating",
		    "lat": 12.931466048533533,
		    "lng": 100.86260895029525,
		    "name": "Aroma Cafe ",
		    "openingTimes": [
		      {
		        "_id": "6425e43ae0dd8621c2ab283b",
		        "closed": false,
		        "closing": "7:00pm",
		        "days": "Monday - Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 2,
		    "reviews": [
		      {
		        "_id": "6425e43ae0dd8621c2ab283e",
		        "author": "Cameron Hart",
		        "author_id": "6425e431e0dd8621c2ab26ce",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 4,
		        "review_text": "The coffee at this shop is consistently good, and the wifi is fast and reliable. It's the perfect spot to get some work done while enjoying a great cup of coffee."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab2840",
		        "author": "Kameko Mejia",
		        "author_id": "6425e432e0dd8621c2ab2709",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 3,
		        "review_text": "The wifi was a bit spotty, but the coffee was delicious and the seating was comfortable. It's a great place to relax and read a book."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab2842",
		        "author": "Candice Knowles",
		        "author_id": "6425e434e0dd8621c2ab276d",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to use my phone as a hotspot just to get some work done."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab2844",
		        "author": "Aquila Pierce",
		        "author_id": "6425e433e0dd8621c2ab2749",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab2846",
		        "author": "Chancellor Livingston",
		        "author_id": "6425e433e0dd8621c2ab2733",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is some of the fastest I've ever experienced, and the coffee is delicious. It's the perfect place to work or study."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab2848",
		        "author": "Shaeleigh Padilla",
		        "author_id": "6425e431e0dd8621c2ab26db",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 1,
		        "review_text": "The coffee at this shop was average at best, but the worst part was the terrible wifi. I couldn't even check my email."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab284a",
		        "author": "Cyrus Whitfield",
		        "author_id": "6425e433e0dd8621c2ab272b",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is excellent, and the coffee is consistently good. It's the perfect spot to catch up on some work."
		      }
		    ],
		    "views": 7
		  },
		  {
		    "_id": "6425e43ce0dd8621c2ab288b",
		    "address": " 5678 Willowwood Street",
		    "dist_calc": 1.7769386946248582,
		    "facilities": "Restrooms,Music Ambiance,Cash Registers",
		    "lat": 12.931633099969442,
		    "lng": 100.8621782187105,
		    "name": "Bean Scene ",
		    "openingTimes": [
		      {
		        "_id": "6425e43ce0dd8621c2ab2889",
		        "closed": false,
		        "closing": "8:00pm",
		        "days": "Monday - Saturday",
		        "opening": "7:00am"
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab288a",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 3,
		    "reviews": [
		      {
		        "_id": "6425e43ce0dd8621c2ab288d",
		        "author": "Anne Travis",
		        "author_id": "6425e432e0dd8621c2ab2715",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab288f",
		        "author": "Astra Mckinney",
		        "author_id": "6425e432e0dd8621c2ab2721",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 3,
		        "review_text": "The wifi at this coffee shop could be better, but the coffee was great and the staff was friendly and attentive."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab2891",
		        "author": "Chaney Logan",
		        "author_id": "6425e433e0dd8621c2ab2740",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop was decent, but it did slow down during peak hours. The coffee, however, was consistently good."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab2893",
		        "author": "Aquila Pierce",
		        "author_id": "6425e433e0dd8621c2ab2749",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 2,
		        "review_text": "The coffee shop had a nice ambiance, and while the wifi wasn't the fastest, it was enough to get some work done."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e43be0dd8621c2ab2863",
		    "address": " 2345 Walnutwood Street",
		    "dist_calc": 2.0976083457183603,
		    "facilities": "Outdoor Seating,Barista Station,Espresso Machines,Outdoor Seating",
		    "lat": 12.934454261159935,
		    "lng": 100.86320329816131,
		    "name": "Coffee Culture ",
		    "openingTimes": [
		      {
		        "_id": "6425e43be0dd8621c2ab2861",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": "Monday - Saturday",
		        "opening": "6:00am"
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2862",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e43be0dd8621c2ab2865",
		        "author": "Burton Gregory",
		        "author_id": "6425e431e0dd8621c2ab26d9",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to use my phone as a hotspot just to get some work done."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2867",
		        "author": "Macon Cooper",
		        "author_id": "6425e43be0dd8621c2ab285d",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 1,
		        "review_text": "The coffee was decent, but the terrible wifi ruined my experience at this coffee shop. I won't be coming back."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2869",
		        "author": "Harding Maddox",
		        "author_id": "6425e431e0dd8621c2ab26d7",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab286b",
		        "author": "Vernon Nielsen",
		        "author_id": "6425e432e0dd8621c2ab26f9",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to leave and find another place to get some work done. Save yourself the trouble and go elsewhere."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e43ee0dd8621c2ab28d9",
		    "address": " 1234 Walnutwood Avenue",
		    "dist_calc": 2.1727286897018594,
		    "facilities": "Seating Options,Coffee Machines,Baked Goods",
		    "lat": 12.935140678000757,
		    "lng": 100.86309051332901,
		    "name": "The Coffee Cartel ",
		    "openingTimes": [
		      {
		        "_id": "6425e43ee0dd8621c2ab28d8",
		        "closed": false,
		        "closing": "8:00pm",
		        "days": "Monday - Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 2,
		    "reviews": [
		      {
		        "_id": "6425e43ee0dd8621c2ab28db",
		        "author": "Winifred Cote",
		        "author_id": "6425e434e0dd8621c2ab275e",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 4,
		        "review_text": "The coffee is amazing and the wifi is fast and reliable. This coffee shop has become my new favorite spot for a quick work session."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28dd",
		        "author": "Vernon Nielsen",
		        "author_id": "6425e432e0dd8621c2ab26f9",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 3,
		        "review_text": "The wifi was a bit spotty, but the coffee was delicious and the seating was comfortable. It's a great place to relax and read a book."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28df",
		        "author": "Candice Knowles",
		        "author_id": "6425e434e0dd8621c2ab276d",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop could be better, but the coffee was great and the staff was friendly and attentive."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28e1",
		        "author": "Anne Travis",
		        "author_id": "6425e432e0dd8621c2ab2715",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e438e0dd8621c2ab2804",
		    "address": " 6789 Oakwood Street",
		    "dist_calc": 2.3513225777951243,
		    "facilities": "Baked Goods",
		    "lat": 12.936788536460643,
		    "lng": 100.86239610270913,
		    "name": "Brewed Awakening ",
		    "openingTimes": [
		      {
		        "_id": "6425e438e0dd8621c2ab2803",
		        "closed": false,
		        "closing": "7:00pm",
		        "days": "Monday - Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e438e0dd8621c2ab2806",
		        "author": "Ingrid O'brien",
		        "author_id": "6425e432e0dd8621c2ab270d",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 2,
		        "review_text": "This coffee shop has a nice selection of coffee and pastries, and the wifi was decent enough for me to check my emails."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab2808",
		        "author": "Burton Gregory",
		        "author_id": "6425e431e0dd8621c2ab26d9",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to leave and find another place to get some work done. Save yourself the trouble and go elsewhere."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab280a",
		        "author": "Chase Sharp",
		        "author_id": "6425e435e0dd8621c2ab2785",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 1,
		        "review_text": "The coffee was decent, but the terrible wifi ruined my experience at this coffee shop. I won't be coming back."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab280c",
		        "author": "McKenzie Steele",
		        "author_id": "6425e436e0dd8621c2ab27bb",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 1,
		        "review_text": "I was extremely disappointed with this coffee shop. The wifi was slow and unreliable, making it impossible to get any work done."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab280e",
		        "author": "Astra Mckinney",
		        "author_id": "6425e432e0dd8621c2ab2721",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to use my phone as a hotspot just to get some work done."
		      },
		      {
		        "_id": "6425e438e0dd8621c2ab2810",
		        "author": "Candice Knowles",
		        "author_id": "6425e434e0dd8621c2ab276d",
		        "created_on": "Thu, 30 Mar 2023 19:34:16 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab2812",
		        "author": "Valentine Harvey",
		        "author_id": "6425e433e0dd8621c2ab2747",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the wifi was decent, but the seating could be more comfortable. Overall, it's a nice spot to grab a cup of coffee and get some work done."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab2814",
		        "author": "Robin Little",
		        "author_id": "6425e432e0dd8621c2ab26fb",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 1,
		        "review_text": "The coffee at this shop was average at best, but the worst part was the terrible wifi. I couldn't even check my email."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab2816",
		        "author": "Winifred Cote",
		        "author_id": "6425e434e0dd8621c2ab275e",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 1,
		        "review_text": "I would not recommend this coffee shop for anyone who needs to get work done. The wifi was virtually unusable."
		      }
		    ],
		    "views": 9
		  },
		  {
		    "_id": "6425e43ee0dd8621c2ab28f7",
		    "address": " 9012 Willowwood Avenue",
		    "dist_calc": 2.38116486258279,
		    "facilities": "Barista Station,Seating Options,Specialty Drinks,Barista Station,Cash Registers",
		    "lat": 12.937047962089055,
		    "lng": 100.86259696909462,
		    "name": "The Bean Barn ",
		    "openingTimes": [
		      {
		        "_id": "6425e43ee0dd8621c2ab28f4",
		        "closed": false,
		        "closing": "6:00pm",
		        "days": "Monday - Thursday",
		        "opening": "7:00am"
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28f5",
		        "closed": false,
		        "closing": "8:00pm",
		        "days": " Friday",
		        "opening": "7:00am"
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28f6",
		        "closed": false,
		        "closing": "6:00pm",
		        "days": " Saturday and Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e43ee0dd8621c2ab28f9",
		        "author": "Troy Nielsen",
		        "author_id": "6425e431e0dd8621c2ab26c8",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 1,
		        "review_text": "I was extremely disappointed with this coffee shop. The wifi was slow and unreliable, making it impossible to get any work done."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28fb",
		        "author": "Astra Mckinney",
		        "author_id": "6425e432e0dd8621c2ab2721",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to leave and find another place to get some work done. Save yourself the trouble and go elsewhere."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab28fd",
		        "author": "Cynthia Fowler",
		        "author_id": "6425e438e0dd8621c2ab27f4",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 2,
		        "review_text": "The wifi was a bit spotty, but the coffee was delicious and the seating was comfortable. It's a great place to relax and read a book."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab28ff",
		        "author": "Winifred Cote",
		        "author_id": "6425e434e0dd8621c2ab275e",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e43ce0dd8621c2ab28ae",
		    "address": " 7890 Birchwood Court",
		    "dist_calc": 2.390726126474213,
		    "facilities": "Restrooms",
		    "lat": 12.937068412157563,
		    "lng": 100.86354035757365,
		    "name": "The Grindstone ",
		    "openingTimes": [
		      {
		        "_id": "6425e43ce0dd8621c2ab28ac",
		        "closed": false,
		        "closing": "8:00pm",
		        "days": "Monday - Saturday",
		        "opening": "7:00am"
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab28ad",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 2,
		    "reviews": [
		      {
		        "_id": "6425e43ce0dd8621c2ab28b0",
		        "author": "Burton Gregory",
		        "author_id": "6425e431e0dd8621c2ab26d9",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28b2",
		        "author": "Demetria Harvey",
		        "author_id": "6425e431e0dd8621c2ab26ca",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 2,
		        "review_text": "The coffee at this shop was good, but the wifi was a bit slow. Still, it was a nice place to relax and catch up on some work."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28b4",
		        "author": "Harrison Howe",
		        "author_id": "6425e435e0dd8621c2ab2781",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but the seating could be more comfortable. Overall, it's a nice spot to grab a cup of coffee and get some work done."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28b6",
		        "author": "Eaton Hodges",
		        "author_id": "6425e433e0dd8621c2ab2729",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 1,
		        "review_text": "I was really looking forward to trying this coffee shop, but the wifi was so slow that I couldn't even load a webpage."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e439e0dd8621c2ab2828",
		    "address": " 5678 Birchwood Avenue",
		    "dist_calc": 2.5678370684565244,
		    "facilities": "Menu Displays,Music Ambiance,Tea Selection,Outdoor Seating",
		    "lat": 12.938671557553368,
		    "lng": 100.86347096373187,
		    "name": "The Grind Cafe ",
		    "openingTimes": [
		      {
		        "_id": "6425e439e0dd8621c2ab2827",
		        "closed": false,
		        "closing": "8:00pm",
		        "days": "Monday - Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e439e0dd8621c2ab282a",
		        "author": "Magee Mason",
		        "author_id": "6425e437e0dd8621c2ab27c7",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab282c",
		        "author": "Caryn Daniels",
		        "author_id": "6425e439e0dd8621c2ab282b",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab282e",
		        "author": "Jasmine Cabrera",
		        "author_id": "6425e431e0dd8621c2ab26e3",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 1,
		        "review_text": "I would not recommend this coffee shop for anyone who needs to get work done. The wifi was virtually unusable."
		      },
		      {
		        "_id": "6425e439e0dd8621c2ab2830",
		        "author": "Constance Glenn",
		        "author_id": "6425e433e0dd8621c2ab2731",
		        "created_on": "Thu, 30 Mar 2023 19:34:17 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the wifi was decent, but the seating could be more comfortable. Overall, it's a nice spot to grab a cup of coffee and get some work done."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e433e0dd8621c2ab2744",
		    "address": " 9012 Birchwood Street",
		    "dist_calc": 2.7924629043123943,
		    "facilities": "Free Wi-fi,Power Outlets,Barista Station,Barista Station",
		    "lat": 12.940657420043594,
		    "lng": 100.86393102029227,
		    "name": "Caf\u00e9 Latte ",
		    "openingTimes": [
		      {
		        "_id": "6425e433e0dd8621c2ab2742",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": "Monday - Saturday",
		        "opening": "6:00am"
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2743",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 3,
		    "reviews": [
		      {
		        "_id": "6425e433e0dd8621c2ab2746",
		        "author": "Bianca Salas",
		        "author_id": "6425e431e0dd8621c2ab26d5",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is excellent, and the coffee is consistently good. It's the perfect spot to catch up on some work."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2748",
		        "author": "Valentine Harvey",
		        "author_id": "6425e433e0dd8621c2ab2747",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is some of the fastest I've ever experienced, and the coffee is delicious. It's the perfect place to work or study."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab274a",
		        "author": "Aquila Pierce",
		        "author_id": "6425e433e0dd8621c2ab2749",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab274c",
		        "author": "Zena Rasmussen",
		        "author_id": "6425e433e0dd8621c2ab274b",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the wifi was decent, but the seating could be more comfortable. Overall, it's a nice spot to grab a cup of coffee and get some work done."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e43ce0dd8621c2ab28a3",
		    "address": " 3456 Maplewood Court",
		    "dist_calc": 2.864270353036631,
		    "facilities": "Music Ambiance",
		    "lat": 12.941376588017087,
		    "lng": 100.86293340745111,
		    "name": "Coffee & Co. ",
		    "openingTimes": [
		      {
		        "_id": "6425e43ce0dd8621c2ab28a1",
		        "closed": false,
		        "closing": "8:00pm",
		        "days": "Monday - Saturday",
		        "opening": "7:00am"
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab28a2",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e43ce0dd8621c2ab28a5",
		        "author": "Bianca Salas",
		        "author_id": "6425e431e0dd8621c2ab26d5",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 1,
		        "review_text": "I was really looking forward to trying this coffee shop, but the wifi was so slow that I couldn't even load a webpage."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab28a7",
		        "author": "Wyatt Stephens",
		        "author_id": "6425e432e0dd8621c2ab270b",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 2,
		        "review_text": "The coffee shop had a nice ambiance, and while the wifi wasn't the fastest, it was enough to get some work done."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab28a9",
		        "author": "Eleanor Soto",
		        "author_id": "6425e437e0dd8621c2ab27de",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 1,
		        "review_text": "The coffee was decent, but the terrible wifi ruined my experience at this coffee shop. I won't be coming back."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab28ab",
		        "author": "Cynthia Fowler",
		        "author_id": "6425e438e0dd8621c2ab27f4",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 3,
		        "review_text": "The wifi at this coffee shop was decent, but it did slow down during peak hours. The coffee, however, was consistently good."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e432e0dd8621c2ab2714",
		    "address": " 2345 Cedar Street",
		    "dist_calc": 2.8672775008863387,
		    "facilities": "Outdoor Seating",
		    "lat": 12.941429210299914,
		    "lng": 100.86231652727315,
		    "name": "Perk Up Caf\u00e9 ",
		    "openingTimes": [
		      {
		        "_id": "6425e432e0dd8621c2ab2713",
		        "closed": false,
		        "closing": "7:00pm",
		        "days": "Monday - Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e432e0dd8621c2ab2716",
		        "author": "Anne Travis",
		        "author_id": "6425e432e0dd8621c2ab2715",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 1,
		        "review_text": "I was really looking forward to trying this coffee shop, but the wifi was so slow that I couldn't even load a webpage."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab2718",
		        "author": "Burton Gregory",
		        "author_id": "6425e431e0dd8621c2ab26d9",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 2,
		        "review_text": "The coffee shop had a nice ambiance, and while the wifi wasn't the fastest, it was enough to get some work done."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab271a",
		        "author": "Ingrid O'brien",
		        "author_id": "6425e432e0dd8621c2ab270d",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop was decent, but it did slow down during peak hours. The coffee, however, was consistently good."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab271c",
		        "author": "Ann Wood",
		        "author_id": "6425e432e0dd8621c2ab271b",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop was decent, but not the fastest. However, the comfortable seating and delicious coffee made up for it."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e431e0dd8621c2ab26c7",
		    "address": " 1234 Maple Street",
		    "dist_calc": 3.007464237115097,
		    "facilities": "Tea Selection",
		    "lat": 12.942672668818673,
		    "lng": 100.86276610494166,
		    "name": "The Roasted Bean ",
		    "openingTimes": [
		      {
		        "_id": "6425e431e0dd8621c2ab26c4",
		        "closed": false,
		        "closing": "11:30pm",
		        "days": "Monday - Friday",
		        "opening": "10:00am"
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26c5",
		        "closed": true,
		        "days": "Saturday"
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26c6",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e431e0dd8621c2ab26c9",
		        "author": "Troy Nielsen",
		        "author_id": "6425e431e0dd8621c2ab26c8",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 1,
		        "review_text": "I was extremely disappointed with this coffee shop. The wifi was slow and unreliable, making it impossible to get any work done."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26cb",
		        "author": "Demetria Harvey",
		        "author_id": "6425e431e0dd8621c2ab26ca",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the wifi was decent, but the seating could be more comfortable. Overall, it's a nice spot to grab a cup of coffee and get some work done."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26cd",
		        "author": "Cameran Stuart",
		        "author_id": "6425e431e0dd8621c2ab26cc",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26cf",
		        "author": "Cameron Hart",
		        "author_id": "6425e431e0dd8621c2ab26ce",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 1,
		        "review_text": "The coffee was decent, but the terrible wifi ruined my experience at this coffee shop. I won't be coming back."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e431e0dd8621c2ab26f4",
		    "address": " 3456 Pine Street",
		    "dist_calc": 3.0379556305949693,
		    "facilities": "Music Ambiance,Free Wi-fi,Seating Options",
		    "lat": 12.942935599603212,
		    "lng": 100.86300011547104,
		    "name": "Bean There, Done That ",
		    "openingTimes": [
		      {
		        "_id": "6425e431e0dd8621c2ab26f3",
		        "closed": false,
		        "closing": "5:00pm",
		        "days": "Monday - Sunday",
		        "opening": "9:00am"
		      }
		    ],
		    "rating": 4,
		    "reviews": [
		      {
		        "_id": "6425e431e0dd8621c2ab26f6",
		        "author": "Cameron Hart",
		        "author_id": "6425e431e0dd8621c2ab26ce",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 4,
		        "review_text": "The coffee at this shop was excellent, and the fast wifi made it easy for me to stay connected while I worked."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26f8",
		        "author": "Ruth Solis",
		        "author_id": "6425e431e0dd8621c2ab26f7",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop was fast and reliable, which made it the perfect spot for a quick coffee break and some work."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab26fa",
		        "author": "Vernon Nielsen",
		        "author_id": "6425e432e0dd8621c2ab26f9",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop is my go-to spot for delicious coffee and fast wifi. The staff is friendly and the atmosphere is relaxing."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab26fc",
		        "author": "Robin Little",
		        "author_id": "6425e432e0dd8621c2ab26fb",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 3,
		        "review_text": "The wifi was a bit spotty, but the coffee was delicious and the seating was comfortable. It's a great place to relax and read a book."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e433e0dd8621c2ab2739",
		    "address": " 5678 Cedarwood Street",
		    "dist_calc": 3.0515186227249145,
		    "facilities": "Free Wi-fi,Specialty Drinks",
		    "lat": 12.943074727535876,
		    "lng": 100.86262339336227,
		    "name": "Cup of Joe ",
		    "openingTimes": [
		      {
		        "_id": "6425e433e0dd8621c2ab2737",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": "Monday - Saturday",
		        "opening": "6:00am"
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2738",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 2,
		    "reviews": [
		      {
		        "_id": "6425e433e0dd8621c2ab273b",
		        "author": "Wyatt Stephens",
		        "author_id": "6425e432e0dd8621c2ab270b",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab273d",
		        "author": "Clare Washington",
		        "author_id": "6425e433e0dd8621c2ab273c",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 2,
		        "review_text": "The wifi was a bit spotty, but the coffee was delicious and the seating was comfortable. It's a great place to relax and read a book."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab273f",
		        "author": "Mufutau Conway",
		        "author_id": "6425e431e0dd8621c2ab26f1",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2741",
		        "author": "Chaney Logan",
		        "author_id": "6425e433e0dd8621c2ab2740",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 3,
		        "review_text": "The wifi at this coffee shop was decent, but not the fastest. However, the comfortable seating and delicious coffee made up for it."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e435e0dd8621c2ab278a",
		    "address": " 6789 Apple Street",
		    "dist_calc": 3.1847854629358654,
		    "facilities": "Free Wi-fi,To-go Cups",
		    "lat": 12.944252295498439,
		    "lng": 100.86308049878114,
		    "name": "Rise and Grind ",
		    "openingTimes": [
		      {
		        "_id": "6425e435e0dd8621c2ab2789",
		        "closed": false,
		        "closing": "7:00pm",
		        "days": "Monday - Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e435e0dd8621c2ab278c",
		        "author": "Chaney Logan",
		        "author_id": "6425e433e0dd8621c2ab2740",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to use my phone as a hotspot just to get some work done."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab278e",
		        "author": "Kay Sears",
		        "author_id": "6425e431e0dd8621c2ab26eb",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but the seating could be more comfortable. Overall, it's a nice spot to grab a cup of coffee and get some work done."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab2790",
		        "author": "Ruth Solis",
		        "author_id": "6425e431e0dd8621c2ab26f7",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 1,
		        "review_text": "I would not recommend this coffee shop for anyone who needs to get work done. The wifi was virtually unusable."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab2792",
		        "author": "Chase Sharp",
		        "author_id": "6425e435e0dd8621c2ab2785",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e43be0dd8621c2ab287a",
		    "address": " 1234 Oakwood Avenue",
		    "dist_calc": 3.3355749956234,
		    "facilities": "Specialty Drinks,Restrooms",
		    "lat": 12.945647324233336,
		    "lng": 100.86174436610791,
		    "name": "The Caffeine Fix ",
		    "openingTimes": [
		      {
		        "_id": "6425e43be0dd8621c2ab2876",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": "Monday - Thursday",
		        "opening": "6:30am"
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2877",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": " Friday",
		        "opening": "6:30am"
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2878",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": " Saturday",
		        "opening": "7:30am"
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2879",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": " Sunday",
		        "opening": "7:30am"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e43be0dd8621c2ab287c",
		        "author": "Chase Sharp",
		        "author_id": "6425e435e0dd8621c2ab2785",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 1,
		        "review_text": "The coffee was nothing special, and the wifi was so slow that I couldn't even upload a simple document."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab287e",
		        "author": "Burton Gregory",
		        "author_id": "6425e431e0dd8621c2ab26d9",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the wifi was decent, but the seating could be more comfortable. Overall, it's a nice spot to grab a cup of coffee and get some work done."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2880",
		        "author": "Eleanor Soto",
		        "author_id": "6425e437e0dd8621c2ab27de",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop could be better, but the coffee was great and the staff was friendly and attentive."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2882",
		        "author": "Shaeleigh Padilla",
		        "author_id": "6425e431e0dd8621c2ab26db",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 1,
		        "review_text": "I was extremely disappointed with this coffee shop. The wifi was slow and unreliable, making it impossible to get any work done."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2884",
		        "author": "Graiden Williamson",
		        "author_id": "6425e436e0dd8621c2ab27a1",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 1,
		        "review_text": "I would not recommend this coffee shop for anyone who needs to get work done. The wifi was virtually unusable."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab2886",
		        "author": "Eaton Hodges",
		        "author_id": "6425e433e0dd8621c2ab2729",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to leave and find another place to get some work done. Save yourself the trouble and go elsewhere."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab2888",
		        "author": "Alea Cannon",
		        "author_id": "6425e43ae0dd8621c2ab2857",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      }
		    ],
		    "views": 7
		  },
		  {
		    "_id": "6425e435e0dd8621c2ab2794",
		    "address": " 1234 Willow Street",
		    "dist_calc": 3.487035110875081,
		    "facilities": "Outdoor Seating,Restrooms,Baked Goods,Seating Options",
		    "lat": 12.947008688142704,
		    "lng": 100.8616058634225,
		    "name": "The Coffee Spot ",
		    "openingTimes": [
		      {
		        "_id": "6425e435e0dd8621c2ab2793",
		        "closed": false,
		        "closing": "5:00pm",
		        "days": "Monday - Sunday",
		        "opening": "9:00am"
		      }
		    ],
		    "rating": 3,
		    "reviews": [
		      {
		        "_id": "6425e435e0dd8621c2ab2796",
		        "author": "Bianca Salas",
		        "author_id": "6425e431e0dd8621c2ab26d5",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop has amazing coffee and great wifi. I was able to get a lot of work done in a comfortable and cozy atmosphere."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab2798",
		        "author": "Wyatt Stephens",
		        "author_id": "6425e432e0dd8621c2ab270b",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab279a",
		        "author": "Clare Washington",
		        "author_id": "6425e433e0dd8621c2ab273c",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 3,
		        "review_text": "The wifi was a bit spotty, but the coffee was delicious and the seating was comfortable. It's a great place to relax and read a book."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab279c",
		        "author": "Eaton Hodges",
		        "author_id": "6425e433e0dd8621c2ab2729",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 2,
		        "review_text": "The coffee shop had a nice ambiance, and while the wifi wasn't the fastest, it was enough to get some work done."
		      },
		      {
		        "_id": "6425e436e0dd8621c2ab279e",
		        "author": "Allen Alford",
		        "author_id": "6425e431e0dd8621c2ab26e7",
		        "created_on": "Thu, 30 Mar 2023 19:34:14 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop has a great selection of coffee and pastries, and the fast wifi makes it a great spot to catch up on emails or work."
		      },
		      {
		        "_id": "6425e436e0dd8621c2ab27a0",
		        "author": "Candice Knowles",
		        "author_id": "6425e434e0dd8621c2ab276d",
		        "created_on": "Thu, 30 Mar 2023 19:34:14 GMT",
		        "rating": 4,
		        "review_text": "The coffee at this shop was excellent, and the fast wifi made it easy for me to stay connected while I worked."
		      },
		      {
		        "_id": "6425e436e0dd8621c2ab27a2",
		        "author": "Graiden Williamson",
		        "author_id": "6425e436e0dd8621c2ab27a1",
		        "created_on": "Thu, 30 Mar 2023 19:34:14 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      },
		      {
		        "_id": "6425e436e0dd8621c2ab27a4",
		        "author": "Winifred Cote",
		        "author_id": "6425e434e0dd8621c2ab275e",
		        "created_on": "Thu, 30 Mar 2023 19:34:14 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      },
		      {
		        "_id": "6425e436e0dd8621c2ab27a6",
		        "author": "Cameran Stuart",
		        "author_id": "6425e431e0dd8621c2ab26cc",
		        "created_on": "Thu, 30 Mar 2023 19:34:14 GMT",
		        "rating": 2,
		        "review_text": "The coffee at this shop was good, but the wifi was a bit slow. Still, it was a nice place to relax and catch up on some work."
		      },
		      {
		        "_id": "6425e436e0dd8621c2ab27a8",
		        "author": "Aquila Pierce",
		        "author_id": "6425e433e0dd8621c2ab2749",
		        "created_on": "Thu, 30 Mar 2023 19:34:14 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      }
		    ],
		    "views": 10
		  },
		  {
		    "_id": "6425e436e0dd8621c2ab27c0",
		    "address": " 9012 Ivy Street",
		    "dist_calc": 3.4931644376521285,
		    "facilities": "Espresso Machines,To-go Cups",
		    "lat": 12.946938571637958,
		    "lng": 100.864377001532,
		    "name": "Daily Dose Coffee ",
		    "openingTimes": [
		      {
		        "_id": "6425e436e0dd8621c2ab27bd",
		        "closed": false,
		        "closing": "6:00pm",
		        "days": "Monday - Friday",
		        "opening": "8:00am"
		      },
		      {
		        "_id": "6425e436e0dd8621c2ab27be",
		        "closed": true,
		        "days": "Saturday"
		      },
		      {
		        "_id": "6425e436e0dd8621c2ab27bf",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 2,
		    "reviews": [
		      {
		        "_id": "6425e436e0dd8621c2ab27c2",
		        "author": "Robin Little",
		        "author_id": "6425e432e0dd8621c2ab26fb",
		        "created_on": "Thu, 30 Mar 2023 19:34:14 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      },
		      {
		        "_id": "6425e436e0dd8621c2ab27c4",
		        "author": "Ann Wood",
		        "author_id": "6425e432e0dd8621c2ab271b",
		        "created_on": "Thu, 30 Mar 2023 19:34:14 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27c6",
		        "author": "Wyatt Stephens",
		        "author_id": "6425e432e0dd8621c2ab270b",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 1,
		        "review_text": "I was really looking forward to trying this coffee shop, but the wifi was so slow that I couldn't even load a webpage."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27c8",
		        "author": "Magee Mason",
		        "author_id": "6425e437e0dd8621c2ab27c7",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is some of the fastest I've ever experienced, and the coffee is delicious. It's the perfect place to work or study."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27ca",
		        "author": "Cameron Hart",
		        "author_id": "6425e431e0dd8621c2ab26ce",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to use my phone as a hotspot just to get some work done."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27cc",
		        "author": "Cameran Stuart",
		        "author_id": "6425e431e0dd8621c2ab26cc",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop is my go-to spot for delicious coffee and fast wifi. The staff is friendly and the atmosphere is relaxing."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27ce",
		        "author": "Demetria Harvey",
		        "author_id": "6425e431e0dd8621c2ab26ca",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop could be better, but the coffee was great and the staff was friendly and attentive."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27d0",
		        "author": "Constance Glenn",
		        "author_id": "6425e433e0dd8621c2ab2731",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is excellent, and the coffee is consistently good. It's the perfect spot to catch up on some work."
		      },
		      {
		        "_id": "6425e437e0dd8621c2ab27d2",
		        "author": "Cyrus Whitfield",
		        "author_id": "6425e433e0dd8621c2ab272b",
		        "created_on": "Thu, 30 Mar 2023 19:34:15 GMT",
		        "rating": 1,
		        "review_text": "The coffee was nothing special, and the wifi was so slow that I couldn't even upload a simple document."
		      }
		    ],
		    "views": 9
		  },
		  {
		    "_id": "6425e43ae0dd8621c2ab284c",
		    "address": " 7890 Maplewood Avenue",
		    "dist_calc": 3.611287768261138,
		    "facilities": "Free Wi-fi,Music Ambiance,Menu Displays,Barista Station",
		    "lat": 12.94795467491166,
		    "lng": 100.86490891520127,
		    "name": "The Coffee Collective ",
		    "openingTimes": [
		      {
		        "_id": "6425e43ae0dd8621c2ab284b",
		        "closed": false,
		        "closing": "7:00pm",
		        "days": "Monday - Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e43ae0dd8621c2ab284e",
		        "author": "Troy Nielsen",
		        "author_id": "6425e431e0dd8621c2ab26c8",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 2,
		        "review_text": "This coffee shop has a nice selection of coffee and pastries, and the wifi was decent enough for me to check my emails."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab2850",
		        "author": "Kameko Mejia",
		        "author_id": "6425e432e0dd8621c2ab2709",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 2,
		        "review_text": "The wifi was a bit spotty, but the coffee was delicious and the seating was comfortable. It's a great place to relax and read a book."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab2852",
		        "author": "Cyrus Whitfield",
		        "author_id": "6425e433e0dd8621c2ab272b",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the atmosphere was cozy, but the wifi was a bit slow. Still, I was able to get some work done."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab2854",
		        "author": "Shad Gilliam",
		        "author_id": "6425e43ae0dd8621c2ab2853",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 1,
		        "review_text": "I would not recommend this coffee shop for anyone who needs to get work done. The wifi was virtually unusable."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab2856",
		        "author": "Chaney Logan",
		        "author_id": "6425e433e0dd8621c2ab2740",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop was decent, but not the fastest. However, the comfortable seating and delicious coffee made up for it."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab2858",
		        "author": "Alea Cannon",
		        "author_id": "6425e43ae0dd8621c2ab2857",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 1,
		        "review_text": "I was extremely disappointed with this coffee shop. The wifi was slow and unreliable, making it impossible to get any work done."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab285a",
		        "author": "Caryn Daniels",
		        "author_id": "6425e439e0dd8621c2ab282b",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 1,
		        "review_text": "The coffee was overpriced and the wifi was practically non-existent. I won't be coming back to this coffee shop."
		      },
		      {
		        "_id": "6425e43ae0dd8621c2ab285c",
		        "author": "Kay Sears",
		        "author_id": "6425e431e0dd8621c2ab26eb",
		        "created_on": "Thu, 30 Mar 2023 19:34:18 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop has a great selection of coffee and pastries, and the fast wifi makes it a great spot to catch up on emails or work."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab285e",
		        "author": "Macon Cooper",
		        "author_id": "6425e43be0dd8621c2ab285d",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e43be0dd8621c2ab2860",
		        "author": "Harrison Howe",
		        "author_id": "6425e435e0dd8621c2ab2781",
		        "created_on": "Thu, 30 Mar 2023 19:34:19 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      }
		    ],
		    "views": 10
		  },
		  {
		    "_id": "6425e43de0dd8621c2ab28b9",
		    "address": " 2345 Sprucewood Street",
		    "dist_calc": 3.9229739852226158,
		    "facilities": "Tea Selection,Restrooms,Specialty Drinks,Espresso Machines,Baked Goods",
		    "lat": 12.950922183571363,
		    "lng": 100.86195764896974,
		    "name": "Coffee Quest ",
		    "openingTimes": [
		      {
		        "_id": "6425e43de0dd8621c2ab28b7",
		        "closed": false,
		        "closing": "8:00pm",
		        "days": "Monday - Saturday",
		        "opening": "7:00am"
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28b8",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 3,
		    "reviews": [
		      {
		        "_id": "6425e43de0dd8621c2ab28bb",
		        "author": "Burton Gregory",
		        "author_id": "6425e431e0dd8621c2ab26d9",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 4,
		        "review_text": "The coffee is amazing and the wifi is fast and reliable. This coffee shop has become my new favorite spot for a quick work session."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28bd",
		        "author": "Zena Rasmussen",
		        "author_id": "6425e433e0dd8621c2ab274b",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28bf",
		        "author": "Ann Wood",
		        "author_id": "6425e432e0dd8621c2ab271b",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 3,
		        "review_text": "The coffee shop had a nice ambiance, and while the wifi wasn't the fastest, it was enough to get some work done."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28c1",
		        "author": "Willow Chan",
		        "author_id": "6425e439e0dd8621c2ab281f",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop has amazing coffee and great wifi. I was able to get a lot of work done in a comfortable and cozy atmosphere."
		      }
		    ],
		    "views": 4
		  },
		  {
		    "_id": "6425e433e0dd8621c2ab2751",
		    "address": " 3456 Maplewood Street",
		    "dist_calc": 4.166783162431244,
		    "facilities": "Baked Goods,Tea Selection,Power Outlets,Cash Registers",
		    "lat": 12.952934978477236,
		    "lng": 100.86526605574237,
		    "name": "Buzz Caf\u00e9 ",
		    "openingTimes": [
		      {
		        "_id": "6425e433e0dd8621c2ab274d",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": "Monday - Thursday",
		        "opening": "6:30am"
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab274e",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": " Friday",
		        "opening": "6:30am"
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab274f",
		        "closed": false,
		        "closing": "10:00pm",
		        "days": " Saturday",
		        "opening": "7:30am"
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2750",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": " Sunday",
		        "opening": "7:30am"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e434e0dd8621c2ab2753",
		        "author": "Valentine Harvey",
		        "author_id": "6425e433e0dd8621c2ab2747",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 1,
		        "review_text": "The coffee at this shop was average at best, but the worst part was the terrible wifi. I couldn't even check my email."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab2755",
		        "author": "Burton Gregory",
		        "author_id": "6425e431e0dd8621c2ab26d9",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 1,
		        "review_text": "I was really looking forward to trying this coffee shop, but the wifi was so slow that I couldn't even load a webpage."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab2757",
		        "author": "Mufutau Conway",
		        "author_id": "6425e431e0dd8621c2ab26f1",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 2,
		        "review_text": "The wifi was a bit spotty, but the coffee was delicious and the seating was comfortable. It's a great place to relax and read a book."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab2759",
		        "author": "Troy Nielsen",
		        "author_id": "6425e431e0dd8621c2ab26c8",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab275b",
		        "author": "Chancellor Livingston",
		        "author_id": "6425e433e0dd8621c2ab2733",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 1,
		        "review_text": "The coffee was nothing special, and the wifi was so slow that I couldn't even upload a simple document."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab275d",
		        "author": "Cyrus Whitfield",
		        "author_id": "6425e433e0dd8621c2ab272b",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 2,
		        "review_text": "The coffee shop had a nice ambiance, and while the wifi wasn't the fastest, it was enough to get some work done."
		      },
		      {
		        "_id": "6425e434e0dd8621c2ab275f",
		        "author": "Winifred Cote",
		        "author_id": "6425e434e0dd8621c2ab275e",
		        "created_on": "Thu, 30 Mar 2023 19:34:12 GMT",
		        "rating": 1,
		        "review_text": "I would not recommend this coffee shop for anyone who needs to get work done. The wifi was virtually unusable."
		      }
		    ],
		    "views": 7
		  },
		  {
		    "_id": "6425e43de0dd8621c2ab28c3",
		    "address": " 6789 Cedarwood Court",
		    "dist_calc": 4.297380109548015,
		    "facilities": "Coffee Machines,Restrooms,Cash Registers",
		    "lat": 12.954288307034595,
		    "lng": 100.86144571593289,
		    "name": "The Daily Grindhouse ",
		    "openingTimes": [
		      {
		        "_id": "6425e43de0dd8621c2ab28c2",
		        "closed": false,
		        "closing": "7:00pm",
		        "days": "Monday - Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 4,
		    "reviews": [
		      {
		        "_id": "6425e43de0dd8621c2ab28c5",
		        "author": "Allen Alford",
		        "author_id": "6425e431e0dd8621c2ab26e7",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop is my go-to spot for delicious coffee and fast wifi. The staff is friendly and the atmosphere is relaxing."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28c7",
		        "author": "Samson Flowers",
		        "author_id": "6425e43de0dd8621c2ab28c6",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 3,
		        "review_text": "The coffee shop had a nice ambiance, and while the wifi wasn't the fastest, it was enough to get some work done."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28c9",
		        "author": "Chaney Logan",
		        "author_id": "6425e433e0dd8621c2ab2740",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is excellent, and the coffee is consistently good. It's the perfect spot to catch up on some work."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28cb",
		        "author": "Demetria Harvey",
		        "author_id": "6425e431e0dd8621c2ab26ca",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 5,
		        "review_text": "The coffee at this shop was excellent, and the fast wifi made it easy for me to stay connected while I worked."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28cd",
		        "author": "Cameron Hart",
		        "author_id": "6425e431e0dd8621c2ab26ce",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop has a great selection of coffee and pastries, and the fast wifi makes it a great spot to catch up on emails or work."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28cf",
		        "author": "Malcolm Mclean",
		        "author_id": "6425e431e0dd8621c2ab26e9",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop has amazing coffee and great wifi. I was able to get a lot of work done in a comfortable and cozy atmosphere."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28d1",
		        "author": "Rudyard Bender",
		        "author_id": "6425e43de0dd8621c2ab28d0",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 5,
		        "review_text": "The coffee at this shop is consistently good, and the wifi is fast and reliable. It's the perfect spot to get some work done while enjoying a great cup of coffee."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28d3",
		        "author": "Hoyt Richardson",
		        "author_id": "6425e431e0dd8621c2ab26ef",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e43de0dd8621c2ab28d5",
		        "author": "Astra Mckinney",
		        "author_id": "6425e432e0dd8621c2ab2721",
		        "created_on": "Thu, 30 Mar 2023 19:34:21 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is some of the fastest I've ever experienced, and the coffee is delicious. It's the perfect place to work or study."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28d7",
		        "author": "Alea Cannon",
		        "author_id": "6425e43ae0dd8621c2ab2857",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 3,
		        "review_text": "The coffee at this shop was good, but the wifi was a bit slow. Still, it was a nice place to relax and catch up on some work."
		      }
		    ],
		    "views": 10
		  },
		  {
		    "_id": "6425e431e0dd8621c2ab26e0",
		    "address": " 9012 Oak Street",
		    "dist_calc": 4.331736282791984,
		    "facilities": "Barista Station,Power Outlets",
		    "lat": 12.954534046347154,
		    "lng": 100.86377192090026,
		    "name": "Caffeine Connection ",
		    "openingTimes": [
		      {
		        "_id": "6425e431e0dd8621c2ab26dd",
		        "closed": false,
		        "closing": "7:00pm",
		        "days": "Monday - Friday",
		        "opening": "7:00am"
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26de",
		        "closed": true,
		        "days": "Saturday"
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26df",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e431e0dd8621c2ab26e2",
		        "author": "Shaeleigh Padilla",
		        "author_id": "6425e431e0dd8621c2ab26db",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 2,
		        "review_text": "This coffee shop has a nice selection of coffee and pastries, and the wifi was decent enough for me to check my emails."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26e4",
		        "author": "Jasmine Cabrera",
		        "author_id": "6425e431e0dd8621c2ab26e3",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 1,
		        "review_text": "I was extremely disappointed with this coffee shop. The wifi was slow and unreliable, making it impossible to get any work done."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26e6",
		        "author": "Demetria Harvey",
		        "author_id": "6425e431e0dd8621c2ab26ca",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 1,
		        "review_text": "The coffee was overpriced and the wifi was practically non-existent. I won't be coming back to this coffee shop."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26e8",
		        "author": "Allen Alford",
		        "author_id": "6425e431e0dd8621c2ab26e7",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 1,
		        "review_text": "The coffee was decent, but the terrible wifi ruined my experience at this coffee shop. I won't be coming back."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26ea",
		        "author": "Malcolm Mclean",
		        "author_id": "6425e431e0dd8621c2ab26e9",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26ec",
		        "author": "Kay Sears",
		        "author_id": "6425e431e0dd8621c2ab26eb",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to leave and find another place to get some work done. Save yourself the trouble and go elsewhere."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26ee",
		        "author": "Cameron Hart",
		        "author_id": "6425e431e0dd8621c2ab26ce",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 1,
		        "review_text": "I was really looking forward to trying this coffee shop, but the wifi was so slow that I couldn't even load a webpage."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26f0",
		        "author": "Hoyt Richardson",
		        "author_id": "6425e431e0dd8621c2ab26ef",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop was decent, but it did slow down during peak hours. The coffee, however, was consistently good."
		      },
		      {
		        "_id": "6425e431e0dd8621c2ab26f2",
		        "author": "Mufutau Conway",
		        "author_id": "6425e431e0dd8621c2ab26f1",
		        "created_on": "Thu, 30 Mar 2023 19:34:09 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      }
		    ],
		    "views": 9
		  },
		  {
		    "_id": "6425e43ce0dd8621c2ab2896",
		    "address": " 9012 Cherrywood Street",
		    "dist_calc": 4.343106721262231,
		    "facilities": "Menu Displays,Menu Displays,Menu Displays",
		    "lat": 12.954619614121516,
		    "lng": 100.86405646570985,
		    "name": "Coffee Emporium ",
		    "openingTimes": [
		      {
		        "_id": "6425e43ce0dd8621c2ab2894",
		        "closed": false,
		        "closing": "8:00pm",
		        "days": "Monday - Saturday",
		        "opening": "7:00am"
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab2895",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 3,
		    "reviews": [
		      {
		        "_id": "6425e43ce0dd8621c2ab2898",
		        "author": "Kameko Mejia",
		        "author_id": "6425e432e0dd8621c2ab2709",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop has amazing coffee and great wifi. I was able to get a lot of work done in a comfortable and cozy atmosphere."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab289a",
		        "author": "McKenzie Steele",
		        "author_id": "6425e436e0dd8621c2ab27bb",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop could be better, but the coffee was great and the staff was friendly and attentive."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab289c",
		        "author": "Jasmine Cabrera",
		        "author_id": "6425e431e0dd8621c2ab26e3",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop has a great selection of coffee and pastries, and the fast wifi makes it a great spot to catch up on emails or work."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab289e",
		        "author": "Zena Rasmussen",
		        "author_id": "6425e433e0dd8621c2ab274b",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 2,
		        "review_text": "The coffee at this shop was good, but the wifi was a bit slow. Still, it was a nice place to relax and catch up on some work."
		      },
		      {
		        "_id": "6425e43ce0dd8621c2ab28a0",
		        "author": "Graiden Williamson",
		        "author_id": "6425e436e0dd8621c2ab27a1",
		        "created_on": "Thu, 30 Mar 2023 19:34:20 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      }
		    ],
		    "views": 5
		  },
		  {
		    "_id": "6425e434e0dd8621c2ab2778",
		    "address": " 2345 Orange Street",
		    "dist_calc": 4.7501716034963595,
		    "facilities": "Tea Selection,Coffee Machines,Menu Displays",
		    "lat": 12.958347066497813,
		    "lng": 100.86239126874749,
		    "name": "Mocha Magic ",
		    "openingTimes": [
		      {
		        "_id": "6425e434e0dd8621c2ab2777",
		        "closed": false,
		        "closing": "5:00pm",
		        "days": "Monday - Sunday",
		        "opening": "9:00am"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e435e0dd8621c2ab277a",
		        "author": "Cyrus Whitfield",
		        "author_id": "6425e433e0dd8621c2ab272b",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 1,
		        "review_text": "The coffee at this shop was average at best, but the worst part was the terrible wifi. I couldn't even check my email."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab277c",
		        "author": "Vernon Nielsen",
		        "author_id": "6425e432e0dd8621c2ab26f9",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 1,
		        "review_text": "The coffee was nothing special, and the wifi was so slow that I couldn't even upload a simple document."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab277e",
		        "author": "Eaton Hodges",
		        "author_id": "6425e433e0dd8621c2ab2729",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop could be better, but the coffee was great and the staff was friendly and attentive."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab2780",
		        "author": "Bianca Salas",
		        "author_id": "6425e431e0dd8621c2ab26d5",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 2,
		        "review_text": "The wifi at this coffee shop was decent, but not the fastest. However, the comfortable seating and delicious coffee made up for it."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab2782",
		        "author": "Harrison Howe",
		        "author_id": "6425e435e0dd8621c2ab2781",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 1,
		        "review_text": "I came to this coffee shop to get some work done, but the wifi was so slow that I ended up leaving after only a few minutes."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab2784",
		        "author": "Ruth Solis",
		        "author_id": "6425e431e0dd8621c2ab26f7",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 1,
		        "review_text": "The coffee was decent, but the terrible wifi ruined my experience at this coffee shop. I won't be coming back."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab2786",
		        "author": "Chase Sharp",
		        "author_id": "6425e435e0dd8621c2ab2785",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 1,
		        "review_text": "I was extremely disappointed with this coffee shop. The wifi was slow and unreliable, making it impossible to get any work done."
		      },
		      {
		        "_id": "6425e435e0dd8621c2ab2788",
		        "author": "Allen Alford",
		        "author_id": "6425e431e0dd8621c2ab26e7",
		        "created_on": "Thu, 30 Mar 2023 19:34:13 GMT",
		        "rating": 1,
		        "review_text": "I was really looking forward to trying this coffee shop, but the wifi was so slow that I couldn't even load a webpage."
		      }
		    ],
		    "views": 8
		  },
		  {
		    "_id": "6425e432e0dd8621c2ab271e",
		    "address": " 6789 Birch Street",
		    "dist_calc": 4.82745569471146,
		    "facilities": "Baked Goods,Outdoor Seating,Seating Options",
		    "lat": 12.95885307070517,
		    "lng": 100.86573915851635,
		    "name": "Java Junkies ",
		    "openingTimes": [
		      {
		        "_id": "6425e432e0dd8621c2ab271d",
		        "closed": false,
		        "closing": "7:00pm",
		        "days": "Monday - Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 1,
		    "reviews": [
		      {
		        "_id": "6425e432e0dd8621c2ab2720",
		        "author": "Demetria Harvey",
		        "author_id": "6425e431e0dd8621c2ab26ca",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to use my phone as a hotspot just to get some work done."
		      },
		      {
		        "_id": "6425e432e0dd8621c2ab2722",
		        "author": "Astra Mckinney",
		        "author_id": "6425e432e0dd8621c2ab2721",
		        "created_on": "Thu, 30 Mar 2023 19:34:10 GMT",
		        "rating": 1,
		        "review_text": "I would not recommend this coffee shop for anyone who needs to get work done. The wifi was virtually unusable."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2724",
		        "author": "Shaeleigh Padilla",
		        "author_id": "6425e431e0dd8621c2ab26db",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 1,
		        "review_text": "I was extremely disappointed with this coffee shop. The wifi was slow and unreliable, making it impossible to get any work done."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2726",
		        "author": "Malcolm Mclean",
		        "author_id": "6425e431e0dd8621c2ab26e9",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 1,
		        "review_text": "The coffee at this shop was average at best, but the worst part was the terrible wifi. I couldn't even check my email."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab2728",
		        "author": "Hoyt Richardson",
		        "author_id": "6425e431e0dd8621c2ab26ef",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 1,
		        "review_text": "The coffee was overpriced and the wifi was practically non-existent. I won't be coming back to this coffee shop."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab272a",
		        "author": "Eaton Hodges",
		        "author_id": "6425e433e0dd8621c2ab2729",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 1,
		        "review_text": "The coffee was nothing special, and the wifi was so slow that I couldn't even upload a simple document."
		      },
		      {
		        "_id": "6425e433e0dd8621c2ab272c",
		        "author": "Cyrus Whitfield",
		        "author_id": "6425e433e0dd8621c2ab272b",
		        "created_on": "Thu, 30 Mar 2023 19:34:11 GMT",
		        "rating": 1,
		        "review_text": "The wifi at this coffee shop was so bad that I had to leave and find another place to get some work done. Save yourself the trouble and go elsewhere."
		      }
		    ],
		    "views": 7
		  },
		  {
		    "_id": "6425e43ee0dd8621c2ab28e3",
		    "address": " 5678 Cedarwood Street",
		    "dist_calc": 4.873789516114263,
		    "facilities": "Music Ambiance,Coffee Machines,To-go Cups,Espresso Machines,To-go Cups",
		    "lat": 12.959234979356403,
		    "lng": 100.86611442688597,
		    "name": "Cafe Amore ",
		    "openingTimes": [
		      {
		        "_id": "6425e43ee0dd8621c2ab28e2",
		        "closed": false,
		        "closing": "8:00pm",
		        "days": "Monday - Sunday",
		        "opening": "8:00am"
		      }
		    ],
		    "rating": 4,
		    "reviews": [
		      {
		        "_id": "6425e43ee0dd8621c2ab28e5",
		        "author": "Winifred Cote",
		        "author_id": "6425e434e0dd8621c2ab275e",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 4,
		        "review_text": "The wifi at this coffee shop is fast and reliable, which is perfect for me to get some work done while enjoying a delicious cup of coffee."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28e7",
		        "author": "Harding Maddox",
		        "author_id": "6425e431e0dd8621c2ab26d7",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 4,
		        "review_text": "The coffee is amazing and the wifi is fast and reliable. This coffee shop has become my new favorite spot for a quick work session."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28e9",
		        "author": "Wyatt Stephens",
		        "author_id": "6425e432e0dd8621c2ab270b",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 4,
		        "review_text": "The coffee at this shop was excellent, and the fast wifi made it easy for me to stay connected while I worked."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28eb",
		        "author": "Caryn Daniels",
		        "author_id": "6425e439e0dd8621c2ab282b",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop was fast and reliable, which made it the perfect spot for a quick coffee break and some work."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28ed",
		        "author": "Cynthia Fowler",
		        "author_id": "6425e438e0dd8621c2ab27f4",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 5,
		        "review_text": "This coffee shop has a great selection of coffee and pastries, and the fast wifi makes it a great spot to catch up on emails or work."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28ef",
		        "author": "Kameko Mejia",
		        "author_id": "6425e432e0dd8621c2ab2709",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 3,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28f1",
		        "author": "Ingrid O'brien",
		        "author_id": "6425e432e0dd8621c2ab270d",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop is excellent, and the coffee is consistently good. It's the perfect spot to catch up on some work."
		      },
		      {
		        "_id": "6425e43ee0dd8621c2ab28f3",
		        "author": "Mufutau Conway",
		        "author_id": "6425e431e0dd8621c2ab26f1",
		        "created_on": "Thu, 30 Mar 2023 19:34:22 GMT",
		        "rating": 3,
		        "review_text": "The wifi at this coffee shop could be better, but the coffee was great and the staff was friendly and attentive."
		      }
		    ],
		    "views": 9
		  },
		  {
		    "_id": "6425e43fe0dd8621c2ab2902",
		    "address": " 3456 Birchwood Drive",
		    "dist_calc": 4.898661113666183,
		    "facilities": "Free Wi-fi,Free Wi-fi,Restrooms,Baked Goods",
		    "lat": 12.959532262224744,
		    "lng": 100.86531907455957,
		    "name": "Brew & Chew ",
		    "openingTimes": [
		      {
		        "_id": "6425e43fe0dd8621c2ab2900",
		        "closed": false,
		        "closing": "9:00pm",
		        "days": "Monday - Saturday",
		        "opening": "6:00am"
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab2901",
		        "closed": true,
		        "days": "Sunday"
		      }
		    ],
		    "rating": 4,
		    "reviews": [
		      {
		        "_id": "6425e43fe0dd8621c2ab2904",
		        "author": "Shaeleigh Padilla",
		        "author_id": "6425e431e0dd8621c2ab26db",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 5,
		        "review_text": "The wifi at this coffee shop was fast and reliable, which made it the perfect spot for a quick coffee break and some work."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab2906",
		        "author": "Winifred Cote",
		        "author_id": "6425e434e0dd8621c2ab275e",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 5,
		        "review_text": "The coffee at this shop was excellent, and the fast wifi made it easy for me to stay connected while I worked."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab2908",
		        "author": "Vernon Nielsen",
		        "author_id": "6425e432e0dd8621c2ab26f9",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 2,
		        "review_text": "The coffee was good and the wifi was decent, but it was a bit noisy in the coffee shop which made it hard to focus."
		      },
		      {
		        "_id": "6425e43fe0dd8621c2ab290a",
		        "author": "Eaton Hodges",
		        "author_id": "6425e433e0dd8621c2ab2729",
		        "created_on": "Thu, 30 Mar 2023 19:34:23 GMT",
		        "rating": 4,
		        "review_text": "This coffee shop has a great selection of coffee and pastries, and the fast wifi makes it a great spot to catch up on emails or work."
		      }
		    ],
		    "views": 6
		  }
		];


		return these_locations;
	};

	return {
		locations: locations,
		location: location
	};

};







angular
	.module('myLoc8rApp')
	.service('testData', testData);


})();