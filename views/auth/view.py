# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_bcrypt import Bcrypt
import logging
import models.database

# Initialize the database
db = models.database.DB()

auths = Blueprint('auth', __name__)
bcrypt = Bcrypt()

class User(UserMixin):

    def __init__(self, id):
        self.id = id

@auths.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['pwd']
        try:
            user_valid = db.check_user(username)
            if not user_valid:
                raise ValueError('User Not present')
        except (ValueError):
            flash('Not a valid user', 'error')
            return render_template('login.html')
        else:
            check_pass = db.check_user_pass(username)
            result = bcrypt.check_password_hash(check_pass, password)
            if result == True:
                logging.info("Authenticated session: %s", username)
                user = User(username)
                user_data = db.get_user_profile(username)
                login_user(user)
            else:
                flash('Entered password does not match', 'error')
                return render_template('login.html')

    if request.args.get("next") == None:
        return redirect(url_for('index'))
    else:
		return redirect(request.args.get("next"))

@auths.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logging.info("User logged out: %s", session['user_id'])
    session.pop('username', None)
    logout_user()
    return redirect(url_for('index'))

@auths.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', data=db.get_dept())
    elif request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['uid']
        pw_hash = bcrypt.generate_password_hash(request.form['pwd'])
        phone = request.form['phone']
        dept = request.form['dept']
        sex = request.form['sex']
        if not session.get("logged_in"):
            user_add = db.insert_user(username,fname,lname,email,pw_hash,phone,sex,dept)
            if user_add:
                logging.info("New user added: %s", username)
                flash('Signed up successfully.', 'success')
            else:
                logging.warning("User add failed: %s", username)
                flash('Something went wrong.', 'error')
        return redirect(url_for('signup'))