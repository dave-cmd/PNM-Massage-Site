from . import app
from flask import render_template, request, redirect, url_for
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/terms-and-conditions")
def terms():
    return render_template("terms.html")