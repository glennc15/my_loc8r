import mongoengine as me
import datetime
from passlib.hash import pbkdf2_sha256
import jwt


import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class Users(me.Document):
	name = me.StringField(min_length=1)
	# name = me.StringField()
	email = me.EmailField(unique=True)
	password_hash = me.StringField()


	def set_password(self, password):
		'''

		'''

		self.password_hash = pbkdf2_sha256.hash(password)


	def password_is_valid(self, password):
		'''

		'''

		return self.password_hash == pbkdf2_sha256.hash(password)


	def generate_jwt(self):
		'''

		'''

		jwt_data = {
			"_id": str(self.id),
			'email': self.email,
			'name': self.name,
			'exp': int((datetime.datetime.utcnow() + datetime.timedelta(days=7)).timestamp())
		}


		return jwt.encode(jwt_data, "secret", algorithm="HS256")



