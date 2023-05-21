# myLoc8r

myLoc8r is my implementation of the Loc8r app built by Simon Holmes in his excellent book [Getting MEAN with Mongo, Express, Angular, and Node](https://www.manning.com/books/getting-mean-with-mongo-express-angular-and-node), 1st edition.  


MyLoc8r is a location-based app that helps you find **FICTIONAL** coffee shops and cafes in your area that offer WiFi. By utilizing geolocation data from your browser, MyLoc8r retrieves a list of nearby locations through an API and presents them within the client app. All locations are conveniently displayed on a map, and a columnar view provides summary information, such as distance from your current location, available facilities, ratings, review counts, a snippet from the top review, and indications of whether each location is open or closed. Furthermore, the app includes filters to refine the displayed locations based on your desired facilities.

For each location, you can access detailed information, including a location map, operating hours, and comprehensive reviews. The app also offers convenient controls to log in or register and to add your own review.

You can see myLoc8r in action [here!](https://myloc8r.onrender.com)

My implementation differs from Simon's in the following ways:

1. The back end API is build with [Python Flask](https://flask.palletsprojects.com/en/2.3.x/) instead of Node/Express
2. [MongoEngine](https://docs.mongoengine.org/) is the Object-Document mapper.
3. [Bootstrap 5](https://getbootstrap.com/) is the front end toolkit.
3. [Mapbox](https://www.mapbox.com/) is used instead of Google maps.
4. Uses Python [unittest](https://docs.python.org/3/library/unittest.html) - Unit testing framework and [Requests](https://pypi.org/project/requests/) for API testing.
6. All images and artwork used in MyLoc8r are sourced from [freepik.com](https://www.freepik.com/)