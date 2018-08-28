import os
import ConfigParser

default_conf = os.path.join('etc', 'app.cfg')
conf_present = os.path.isfile(default_conf)
if not conf_present:
	logging.critical("Database config not found at:", os.path.abspath(default_conf))
	sys.exit(1)

# Read configuration from config file
cp = ConfigParser.ConfigParser()
cp.read(default_conf)
try:
	dbhost = cp.get('database', 'db_host')
	dbuser = cp.get('database', 'db_user')
	dbpwd = cp.get('database', 'db_pass')
except Exception as e:
	print "Config error:",e
	sys.exit(1)


SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/new" % (dbuser,dbpwd,dbhost)
CELERY_BROKER = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp://'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
