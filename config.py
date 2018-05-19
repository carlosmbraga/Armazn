import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql://root:123qweasdzxc@localhost:3306/armazn'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = os.urandom(24)
