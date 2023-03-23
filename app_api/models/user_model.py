import mongoengine as me


class User(me.EmbeddedDocument):
	name = me.StringField(min_length=1)
	# name = me.StringField()
	email = me.EmailField()
	# hash = me.StringField()


	def setPassword(self, password):
		'''

		'''

		pass 

