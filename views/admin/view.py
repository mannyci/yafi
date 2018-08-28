from flask import Blueprint
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash, jsonify
from flask_login import LoginManager, UserMixin, login_required
from models.database import db, Users

admin = Blueprint('admin', __name__)

@admin.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user_profile(username):
    print username
    if request.method == 'GET':
        return render_template("user.html", user=Users.query.filter_by(username=username).first())

@admin.route('/user/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit(username):
    if request.method == 'GET':
        return render_template("user_edit.html", user=Users.query.filter_by(username=username).first())
    else:
        return redirect(url_for('admin.user_profile', username=username))

@admin.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if request.method == 'GET':
        return render_template("users.html", data=Users.query.all())
    else:
        print request.form
        return redirect(url_for('user_profile', username=username))

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def departments():
    if request.method == 'GET':
        return render_template("departments.html", data=db.get_dept())
    else:
        result = db.add_dept(request.form['dept-name'],request.form['dept-desc'])
        if result:
            logging.info("New department added: %s", request.form['dept-name'])
            flash('Department added successfully.', 'success')
        else:
            logging.warning("Department add failed: %s", request.form['dept-name'])
            flash('Something went wrong.', 'error')
        return redirect(url_for('departments'))
