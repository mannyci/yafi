# import mysql.connector as mysql
# from mysql.connector import errorcode
import MySQLdb
import MySQLdb.cursors
import os
import ConfigParser
import sys
import logging


class DB(object):
	def __init__(self):
		self.default_conf = os.path.join('etc', 'app.cfg')
		conf_present = os.path.isfile(self.default_conf)
		if not conf_present:
			logging.critical("Database config not found at:", os.path.abspath(self.default_conf))
			sys.exit(1)

		self.read_config()
		self.connect()

	def read_config(self):
		# Set defaults if not in config
		defaults = {
			u'db_host': u'localhost',
			u'db_user': u'root',
			u'db_pass': u'root'
		}
		# Read configuration from config file
		cp = ConfigParser.ConfigParser(defaults)
		cp.read(self.default_conf)
		self.config = cp
		try:
			self.host = self.config.get('database', 'db_host')
			self.user = self.config.get('database', 'db_user')
			self.pwd = self.config.get('database', 'db_pass')
		except Exception as e:
			print "Config error:",e
			sys.exit(1)

	def connect(self):
		try:
			logging.info("Connecting to database: Host=%s User=%s", self.host, self.user)
			self.db = MySQLdb.connect(user=self.user, passwd=self.pwd, host=self.host, db='users', cursorclass=MySQLdb.cursors.DictCursor)
			self.cur = self.db.cursor()
		except Exception,e:
			logging.error(e)
			sys.exit(1)

	def setup(self):
		logging.info("Initializing database and tables")
		tables = {}
		tables['users'] = (
		    "CREATE TABLE IF NOT EXISTS users ("
		    "serial int(10) not null AUTO_INCREMENT unique key,"
		    "id varchar(8) primary key,"
		    "first_name text not null,"
		    "last_name text not null,"
		    "email text not null,"
		    "password text not null,"
		    "phone text not null,"
		    "sex text not null,"
		    "depertment text not null)")

		tables['depertment'] = (
		    "CREATE TABLE IF NOT EXISTS depertment ("
		    "serial int(10) not null AUTO_INCREMENT unique key,"
		    "name varchar(20) primary key,"
			"description text not null)")

		# Create tables if not present
		for name, table in tables.iteritems():
		    try:
		        self.cur.execute(table)
		        self.db.commit()
		    except Exception,e:
		        logging.error(e)

	def insert_user(self,username,fname,lname,email,password,phone,sex,dept):
	    query = ("INSERT INTO users "
	            "(id,first_name,last_name,email,password,phone,sex,depertment)"
	            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
	    data = (username,fname,lname,email,password,phone,sex,dept)
	    try:
	        self.cur.execute(query, data)
	        self.db.commit()
	        return True
	    except Exception,e:
			logging.error(e)
			return False

	def check_user(self,user):
	    self.cur.execute("""SELECT id from users WHERE id='%s'""" % (user))
	    rows = self.cur.fetchone()
	    if rows:
	        return True
	    else:
			return False

	def check_user_pass(self,user):
	    self.cur.execute("""SELECT password FROM users WHERE id='%s'""" % (user)) 
	    rows = self.cur.fetchall()
	    for row in rows:
	        dbpass = row['password']
		return dbpass


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
