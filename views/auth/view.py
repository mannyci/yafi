# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from models.database import db, Users

auths = Blueprint('auth', __name__)

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
        user = Users.query.filter_by(username=username).first()
        if not user:
            flash('Not a valid user', 'error')
            return render_template('login.html')
        else:
            pw_hash = user.password
            if check_password_hash(pw_hash, password):
                # The hash matches the password in the database log the user in
                session['user'] = username
                flash('Login was succesfull')
                logging.info("Authenticated session: %s", username)
                user = User(username)
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
    session.pop('user')
    logout_user()
    return redirect(url_for('index'))

@auths.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['uid']
        password = generate_password_hash(request.form['pwd'])
        phone = request.form['phone']
        sex = request.form['sex']
        if not session.get("logged_in"):
            user = Users(username=username,fname=fname,lname=lname,email=email,password=password,phone=phone,sex=sex)
            db.session.add(user)
            db.session.commit()
            flash('Signed up successfully.', 'success')
        return redirect(url_for('auth.signup'))