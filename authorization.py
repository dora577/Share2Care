from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import Users
from flask_login import login_user, logout_user, login_required
from main import cart_prods

auth = Blueprint('auth', __name__)


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():


    email = request.form.get('email')
    name = request.form.get('name')
    surname = request.form.get('surname')
    password = request.form.get('password')
    isDriver = 1 if request.form.get('isDriver') else 0

    user = Users.query.filter_by(email=email).first() 

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    
    new_user = Users(email=email, name=name,surname = surname, password=password, isDriver = isDriver)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))



@auth.route('/login')
def login():
   
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
   
    email = request.form.get('email')
    password = request.form.get('password')


    user = Users.query.filter_by(email=email).first()

  
    if not user or not user.password == password:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.mywishlist_update'))



@auth.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('main.products'))