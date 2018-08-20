import os
import sys
import datetime
import platform
import ConfigParser
from logging.handlers import RotatingFileHandler
import logging
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

# Import blueprints
from views.ui.view import ui
from views.auth.view import auths
from views.admin.view import admin
from views.jobs.view import jobs

# # Initialize database
import models.database
db = models.database.DB()

defaults = {
    u'host': u'manny.com',
    u'port': u'5000',
    u'db_host': u'0.0.0.0',
    u'loglevel': u'info',
    u'logfile': u'var/app.log',
}

class conf(object):
    """docstring for conf"""
    # def __init__(self):
    #     self.read_config()
    def read_config(self):
        # Read configuration from config file
        self.default_conf = os.path.join('etc', 'app.cfg')
        cp = ConfigParser.ConfigParser(defaults)
        cp.read(self.default_conf)
        self.config = cp
        try:
            self.host = self.config.get('app', 'host')
            self.port = self.config.get('app', 'port')
        except Exception as e:
            print "Config error:",e
            sys.exit(1)

class log(object):

    def start_log(self):
        self.default_conf = os.path.join('etc', 'app.cfg')
        cp = ConfigParser.ConfigParser(defaults)
        cp.read(self.default_conf)
        self.config = cp
        self.logfile = self.config.get('log', 'logfile')
        self.loglevel = self.config.get('log', 'loglevel')
        """Configure the default logging module"""
        handler = []
        # Add the log message handler to the logger
        handler.append(RotatingFileHandler(
                      self.logfile, maxBytes=10 * 1024 * 1024, backupCount=4))
        handler.append(logging.StreamHandler())
        # Set up a specific logger with our desired output level
        self.logger = logging.getLogger()
        self.logger.setLevel(self.loglevel.upper())
        for h in handler:
            h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            self.logger.addHandler(h)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)
# Blueprints here
app.register_blueprint(ui, url_prefix='/ui')
app.register_blueprint(auths, url_prefix="/auth")
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(jobs, url_prefix='/jobs')

# Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

class User(UserMixin):

    def __init__(self, id):
        self.id = id

@app.route('/')
def index():
    return redirect(url_for('ui.index'))

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route('/uploads', methods=['GET','POST'])
@login_required
def profile_image():
    if request.method == 'GET':
        return redirect(url_for('edit', username=session['user_id']))
    else:
        print "File request", request.files['photo']
        file = request.files['photo']
        file.save(os.path.join('flaskapp', 'uploads', file.filename))
        return redirect(url_for('profile_image'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=e, type='404'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error=e, type='500'), 500


if __name__ == '__main__':
    conf().read_config()
    log().start_log()
    app.run(debug=True)