import mongoengine as me
import datetime

class ReviewSchema(me.EmbeddedDocument):
	author = me.StringField(required=True)
	rating = me.IntField(required=True, min_value=0, max_value=5)
	reviewSchema_text = me.StringField(required=True)
	created_on = me.DateTimeField(default=datetime.datetime.utcnow)

class OpeningTimeSchema(me.EmbeddedDocument):
	days = me.StringField(required=True)
	opening = me.StringField()
	closing = me.StringField()
	closed = me.BooleanField(default=True)


class LocationSchema(me.Document):
	name = me.StringField(required=True)
	address = me.StringField()
	rating = me.IntField(default=0, min_value=0, max_value=5)
	facilities = me.ListField(me.StringField())
	coords = me.PointField(auto_index=True)
	opening_times = me.EmbeddedDocumentListField(me.EmbeddedDocument(OpeningTimeSchema))
	reviews = me.EmbeddedDocumentListField(me.EmbeddedDocument(Review))
