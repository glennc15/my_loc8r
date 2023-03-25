import mongoengine as me
import datetime
from passlib.hash import pbkdf2_sha256
import jwt
import re 
from dotenv import load_dotenv
import os

import rlcompleter
import pdb 
pdb.Pdb.complete = rlcompleter.Completer(locals()).complete


class Users(me.Document):
	name = me.StringField(min_length=5)
	# name = me.StringField()
	email = me.EmailField(unique=True)
	password_hash = me.StringField()


	def hash_password(self, password):
		'''

		'''

		self.password_hash = pbkdf2_sha256.hash(password)


	def verify_password(self, password):
		'''

		'''

		return pbkdf2_sha256.verify(password, self.password_hash)


	def validate_password(self, password):
		'''
		
		password validation: 
		length: 5 - 20 characters
		requirements:
		1. Must contain a uppercase letter.
		2. Must contain a lowercase letter.
		3. Must contain a digit. 


		'''
		# requires special characters:
		# re.search(r'^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', key)
	

		return re.search(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,20}$', password) != None


	def generate_jwt(self):
		'''

		'''
		load_dotenv()

		jwt_data = {
			"_id": str(self.id),
			'email': self.email,
			'name': self.name,
			'exp': int((datetime.datetime.utcnow() + datetime.timedelta(days=7)).timestamp())
		}



		return jwt.encode(jwt_data, os.environ.get("JWT_SECRETE"), algorithm="HS256")



