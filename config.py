import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql://root:3306@localhost/armazn'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = os.urandom(24)
