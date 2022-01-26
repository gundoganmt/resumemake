from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from resumemake.models import Users
from datetime import datetime
from resumemake import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from utils import only_main

account = Blueprint('account',__name__)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@account.route('/login', methods=['GET', 'POST'])
@only_main()
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.mysites'))
    if request.method == 'POST':
        login_eu = request.form['login-eu']
        password = request.form['login-password']

        if "@" in login_eu:
            user = Users.query.filter_by(email=login_eu).first()
        else:
            user = Users.query.filter_by(username=login_eu).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard.mysites'))
            else:
                flash('Wrong Credentials!')
                return render_template('account/login.html')
        else:
            flash('User not found!')
            return render_template('account/login.html')
    return render_template('account/login.html')

@account.route('/signup', methods=['GET','POST'])
@only_main()
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    if request.method == 'POST':
        username = request.form['register-username']
        email = request.form['register-email']
        password = request.form['register-password']
        confirm = request.form['confirm-password']
        if password != confirm:
            flash('Passwords not matched! Try again')
            return render_template('account/register.html')
        if not username.isalnum():
            flash('username should be alpha numeric!')
            return render_template('account/register.html')
        hashed_password = generate_password_hash(password, method='sha256')
        existing_username = Users.query.filter_by(username=username).first()
        if existing_username is not None:
            flash('Username already being used!')
            return render_template('account/register.html')
        else:
            existing_email = Users.query.filter_by(email=email).first()
            if existing_email is not None:
                flash('Email already being used')
                return render_template('account/register.html')
            else:
                new_user = Users(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('dashboard.mysites'))
    return render_template('account/register.html')

@account.route('/logout')
@login_required
@only_main()
def logout():
    logout_user()
    return redirect(url_for('public.index'))
