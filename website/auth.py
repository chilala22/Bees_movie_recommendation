#this shows that there are a bunch of files available
from flask import Blueprint, render_template,request,flash,redirect,url_for,jsonify,Response
from .models import Users
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user
# setting up the blueprint for the application
auth=Blueprint('auth',__name__)

#setting up routes and urls
@auth.route('/login', methods=['GET','POST'])
def login():
    #getting info from form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # returns first email that matches the email and password
        users = Users.query.filter_by(email=email).first()
        if users:
            if check_password_hash(users.password, password):
                flash('Logged in successfully!', category='success')
                # true until the clears session or browsing history or web server restarts
                login_user(users, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
        
    return render_template("login.html", users=current_user)

@auth.route('/logout')
@login_required #issures that this route is only accessible if the user is logged in
def logout():
    logout_user() #logs out the current user
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    # get data from form
    if request.method == 'POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        lastName=request.form.get('lastName')
        userName=request.form.get('userName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        users = Users.query.filter_by(email=email).first()

        
        # check if information is valid
        if users:
            flash('Email already exists',category='error')
        elif len(email)<3:
            flash('Email is too short, must be more than 3 characters',category='error')
        elif len(firstName)<2:
            flash('First name is too short, must be more than 2 characters',category='error')
        elif len(lastName)<2:
            flash('Last name is too short, must be more than 2 characters',category='error')
        elif password1!=password2:
            flash('Passwords dont\'t match',category='error')
        elif len(password1)<3:
            flash('Password is too short, must be more than 3 characters',category='error')
        else:
            # add user to db
            new_user = Users(first_name=firstName, last_name=lastName, username=userName, email=email,password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user) #adds new user to the db
            db.session.commit() #commit changes to the db
            # true until the clears session or browsing history or web server restarts
            # login_user(users)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
        
    return render_template("sign_up.html",users=current_user)