from app import db
import os
#import unicode
import unicodedata

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(20))
	#session_token = db.Column(db.String(40), index=True) 

	
	@property
	def is_authenticated(self):
		return True
	@property
	def is_active(self):
		return True
	@property
	def is_anonymous(self):
		return False
	
	def get_id(self):
		#self.session_token = os.urandom(64).decode('utf-8', 'ignore')
		return str(self.id)
		
	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email

	def __repr__(self):
		return "<User %r>" % self.username


class File(db.Model):
	__tablename__ = "files"

	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(50), unique=True)
	size = db.Column(db.Numeric, unique=True)
	content = db.Column(db.Text)
	owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	owner = db.relationship('User', foreign_keys=owner_id)

	def __init__(self, filename, size, content, owner_id):
		self.filename = filename
		self.size = size
		self.content = content
		self.owner_id = owner_id

	def __repr__(self):
		return "<File %r>" % self.filename
