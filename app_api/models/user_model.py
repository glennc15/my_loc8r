import mongoengine as me


import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class User(me.EmbeddedDocument):
	name = me.StringField(min_length=1)
	# name = me.StringField()
	email = me.EmailField()
	hash = me.StringField()


	def set_password(self, password):
		'''

		'''

		pdb.set_trace()

