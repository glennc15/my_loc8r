# myLoc8r

myLoc8r is my implementation of the Loc8r app built by Simon Holmes in his excellent book [Getting MEAN with Mongo, Express, Angular, and Node](https://www.manning.com/books/getting-mean-with-mongo-express-angular-and-node), 1st edition.  

MyLoc8r is a dynamic and user-friendly single-page application designed to help users discover the best **FICTIONAL** coffee shops and cafes with Wifi near their location. Using Geolocation data from the browser, MyLoc8r displays a list of nearby **FICTIONAL** coffee shops and cafes, complete with helpful filters to narrow down the search results by available facilities at each location.

In addition to providing basic information about each location, MyLoc8r also offers in-depth details, such as reviews from other users, operating hours, map details, and a full list of onsite facilities. Users can easily create an account to leave their own reviews and ratings for their favorite **FICTIONAL** coffee shops and cafes, helping others in the community make informed decisions about where to go for their next caffeine fix.

MyLoc8r is an excellent tool for coffee lovers who want to explore new places and connect with other enthusiasts in their area. With its intuitive interface and comprehensive features, MyLoc8r makes finding and sharing great coffee experiences easier than ever before.

You can see myLoc8r in action [here!](www.notsure.yet)

My implementation differs from Simon's in the following ways:

1. The back end API is build with [Python Flask](https://flask.palletsprojects.com/en/2.3.x/) instead of Node/Express
2. [MongoEngine](https://docs.mongoengine.org/) is the Object-Document mapper.
3. [Bootstrap 5](https://getbootstrap.com/) is the front end toolkit.
3. [Mapbox](https://www.mapbox.com/) is used instead of Google maps.
4. Uses Python [unittest](https://docs.python.org/3/library/unittest.html) - Unit testing framework and [Requests](https://pypi.org/project/requests/) for API testing.
5. Uses Python [unittest](https://docs.python.org/3/library/unittest.html) - Unit testing framework and [Selenium](https://selenium-python.readthedocs.io/) for front end testing.

6. All images and artwork used in MyLoc8r are sourced from [freepik.com](https://www.freepik.com/)