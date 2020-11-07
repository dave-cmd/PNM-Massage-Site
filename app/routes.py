from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from app.forms import LoginForm


@app.route("/home")
def home():
    return render_template("home.html", title="Home Page")
@app.route("/terms-and-conditions")
def terms():
    return render_template("terms.html",title="Terms Page")

@app.route("/packages")
def packages():
    return render_template("packages.html", title="Packages Page")
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #flash("Error Login")
        return redirect(url_for('home'))

    
    return render_template("login.html", form=form, title="Login Page")