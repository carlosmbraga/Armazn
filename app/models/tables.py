from app import db

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String)

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email

	def __repr__(self):
		return "<User %r>" % self.username


class File(db.Model):
	__tablename__ = "files"

	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String, unique=True)
	size = db.Column(db.Numeric, unique=True)
	owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	owner = db.relationship('User', foreign_keys=owner_id)

	def __init__(self, filename, size, owner_id):
		self.filename = filename
		self.size = size
		self.owner_id = owner_id

	def __repr__(self):
		return "<File %r>" % self.filename
