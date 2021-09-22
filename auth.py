from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # Check username and password against database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 

    login_user(user, remember=remember)
    return redirect(url_for('main.upload'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/admin', methods=['POST'])
@login_required
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Check if user/email already exits in database
    user = User.query.filter_by(email=email).first() 

    # If user exists, redirect back to admin page
    if user:
        flash('Email address already in use!')
        return redirect(url_for('auth.signup_post'))

    # Create user and hash password
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # Add user to database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))