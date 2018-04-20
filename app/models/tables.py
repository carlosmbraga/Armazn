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
