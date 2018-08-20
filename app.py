import os
import sys
import datetime
import platform
# import logging
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

# Import blueprints
from views.ui.view import ui
from views.auth.view import auths
from views.admin.view import admin
from views.jobs.view import jobs

# # Initialize database
# import models.database
# import views
# db = models.database.DB()

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
    app.run(debug=True)