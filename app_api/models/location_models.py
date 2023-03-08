import mongoengine as me
import datetime
from bson import ObjectId

class Review(me.EmbeddedDocument):
	_id = me.ObjectIdField(required=True, default=ObjectId)
	author = me.StringField(required=True)
	rating = me.IntField(required=True, min_value=0, max_value=5)
	reviewSchema_text = me.StringField(required=True)
	created_on = me.DateTimeField(default=datetime.datetime.utcnow)

class OpeningTime(me.EmbeddedDocument):
	_id = me.ObjectIdField(required=True, default=ObjectId)
	days = me.StringField(required=True)
	opening = me.StringField()
	closing = me.StringField()
	closed = me.BooleanField(default=True)


class Location(me.Document):
	name = me.StringField(required=True)
	address = me.StringField()
	rating = me.IntField(default=0, min_value=0, max_value=5)
	facilities = me.StringField()
	coords = me.PointField(auto_index=True)
	openingTimes = me.ListField(me.EmbeddedDocumentField(OpeningTime))
	reviews = me.ListField(me.EmbeddedDocumentField(Review))
	
	# opening_times = me.EmbeddedDocumentListField(me.EmbeddedDocument(OpeningTimeSchema))
	# reviews = me.EmbeddedDocumentListField(me.EmbeddedDocument(ReviewSchema))