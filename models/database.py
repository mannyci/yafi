from flask_sqlalchemy import SQLAlchemy
import MySQLdb
import MySQLdb.cursors
import os
import ConfigParser
import sys
import logging

db = SQLAlchemy()

# Base model that for other models to inherit from
class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Model to store user details
class Users(Base):
	username = db.Column(db.String(50), unique=True)
	fname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(300))  # incase password hash becomes too long
	phone = db.Column(db.String(20))
	sex = db.Column(db.String(10))

	def __repr__(self):
	    return self.username


