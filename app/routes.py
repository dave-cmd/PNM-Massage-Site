from app import app, db
from app.models import User, Post

from app.forms import LoginForm, RegistrationForm, UpdateForm
from flask import render_template, url_for, redirect,jsonify, flash, request
from flask_login import login_user,logout_user,  current_user, login_required
from werkzeug.urls import url_parse


@app.route("/terms-and-conditions")
def terms():
    return render_template("terms.html",title="Terms Page")

@app.route("/packages")
def packages():
    return render_template("packages.html", title="Packages Page")

@app.route('/')
@app.route('/home')
def home():
	if current_user.is_authenticated:
		user= {
		'username': User.query.get(current_user.get_id()).lastname,
		'career': "Developer"
		}
	else:
		user = {
		"username": "Sample User",
		"career": "Sample Career"
		}

	posts = Post.query.order_by(Post.timestamp).all()
	print(posts)

	return render_template('home.html', title="Home Page", user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for("home"))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		
		if user == None or not user.check_password(form.password.data):
			flash("Invalid credentials")
			return redirect(url_for('login'))
		login_user(user, remember = form.remember_me.data)

		#Ensures redirect to desired page after login verification
		next_page = request.args.get('next')

		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('home')

		return redirect(next_page)

	return render_template('login.html', title="Login Page", form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():

	if not current_user.is_authenticated :
		return redirect(url_for("login"))

	user_id = current_user.get_id()
	user = User.query.get(user_id)

	if user.email != "kanjurus30@gmail.com":
		return redirect(url_for("home"))

	flash("Welcome Administrator!")

	return render_template("admin.html", title="Admin Page")



@app.route('/registration', methods=['GET', 'POST'])
def registration():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()

	if form.validate_on_submit():
		user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, phone_number= form.phone_number.data)
		user.set_password(form.password.data)
		print(user.email)

		db.session.add(user)
		db.session.commit()

		return redirect(url_for('login'))

	return render_template("registration.html", title="Registration Page", form = form)



@app.route('/profile', methods=['GET', 'POST'])
@login_required

def profile():
	if not current_user.is_authenticated:
		return redirect('login')

	form = UpdateForm()

	if form.validate_on_submit():

		current_user.firstname = form.firstname.data
		current_user.lastname = form.lastname.data
		current_user.email = form.email.data
		current_user.phone_number = form.phone_number.data
		db.session.commit()

		flash("Profile Information Updated!")
		return redirect(url_for('profile'))
	elif request.method == 'GET':

		form.firstname.data = current_user.firstname
		form.lastname.data = current_user.lastname
		form.phone_number.data = current_user.phone_number
		form.email.data = current_user.email
		

	posts = Post.query.filter_by(user_id= current_user.get_id()).all()
	image = url_for('static', filename='profile_images/'+ current_user.image_pic)


	return render_template("profile.html", title='Profile Page', posts=posts, image=image, form=form)












