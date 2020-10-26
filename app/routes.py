from . import app
from flask import render_template, request, redirect, url_for
@app.route("/home")
def home():
    return render_template("home.html")