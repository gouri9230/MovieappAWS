
from . import auth
from app import db
from app.models import User
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user,login_user, login_required, logout_user
import json
import urllib.request as req

api_key = 'e6ba148a06e13fea97aa690066688f2b'
base_url = "https://api.tmdb.org/3/discover/movie?api_key="+api_key

@auth.route("/signup", methods = ["POST", "GET"])
def signup():
    
    if request.method == "POST":
        firstname = request.form.get("firstname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        
        user = User.query.filter_by(email = email).first()
        if user:
            flash("User with this email already exists!", category="error")
        elif (len(firstname) < 3):
            flash("Name should be atleast 3 characters!", category='error')
        elif len(email) < 3:
            flash("Email should be atleast 3 characters!", category='error')
        elif password != confirmpassword:
            flash("Passwords do not match!", category='error')
        else:
            new_user = User(name = firstname, email = email, password = password)
            db.session.add(new_user)
            db.session.commit()
            flash("User added successfully!", category = 'success')

            return redirect(url_for('auth.login'))
    
    return render_template("authentication/signup.html", user = current_user)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()    
        if user:                                             
            if user.password == password:
                flash("Logged in successfully!", category= 'success')
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                flash("Incorrect password, try again!", category= 'error')
        else:
            flash("Email does not exist.", category= 'error')

    return render_template("authentication/login.html", user = current_user)

@auth.route('/home')
@auth.route("/")
@login_required
def home():
    connection = req.urlopen(base_url)
    data = json.loads(connection.read())
    return render_template("home.html", data = data["results"], user = current_user)
    
    
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
