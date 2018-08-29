from flask import Blueprint
from flask import Flask, redirect, url_for, request, render_template
from flask_login import login_required
from models.database import db, Users

profile = Blueprint('profile', __name__)

@profile.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user_profile(username):
    if request.method == 'GET':
        return render_template("user.html", user=Users.query.filter_by(username=username).first())

@profile.route('/user/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit(username):
    if request.method == 'GET':
        return render_template("user_edit.html", user=Users.query.filter_by(username=username).first())
    else:
        return redirect(url_for('admin.user_profile', username=username))

@profile.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if request.method == 'GET':
        return render_template("users.html", data=Users.query.all())
    else:
        print request.form
        return redirect(url_for('user_profile', username=username))



