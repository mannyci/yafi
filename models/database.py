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

	def get_user_profile(self,username):
	    self.cur.execute("""SELECT id,first_name,last_name,email,phone,depertment,sex FROM users WHERE id='%s'""" % (username)) 
	    rows = self.cur.fetchall()
	    return rows

	def get_users(self):
	    self.cur.execute("""SELECT id,first_name,last_name,email,phone,depertment FROM users""")
	    rows = self.cur.fetchall()
	    return rows

	def get_dept(self):
	    self.cur.execute("""SELECT serial,name,description from depertment""")
	    rows = self.cur.fetchall()
	    return rows

	def add_dept(self,name,desc):
	    try:
	        self.cur.execute(
	          """INSERT INTO depertment (name, description)
	          VALUES (%s, %s)""", (name, desc))
	        self.db.commit()
	        return True
	    except Exception,e:
			logging.error(e)
			return False
