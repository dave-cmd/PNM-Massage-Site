from app import app, db, mail
from app.models import User, Post

from app.forms import LoginForm, RegistrationForm, UpdateForm, RequestResetForm, ResetPasswordForm, BookMassageForm
from flask import render_template, url_for, redirect,jsonify, flash, request
from flask_login import login_user,logout_user,  current_user, login_required
from werkzeug.urls import url_parse
import secrets
from PIL import Image
import os
from flask_mail import Message




@app.route("/terms")
def terms():
    return render_template("terms.html",title="Terms Page")

@app.route('/')
@app.route('/home')
def home():
	"""
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
	"""

	return render_template('home.html', title="Home Page")



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

	if user.email != app.config['ADMINISTRATOR_MAIL']:
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
		flash('Registration successful.')

		return redirect(url_for('login'))

	return render_template("registration.html", title="Registration Page", form = form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


#Save profile picture logic
def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_images', picture_fn)

	#Resize Image
	output_size = (250, 250)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	if not current_user.is_authenticated:
		return redirect(url_for("login"))

	form = UpdateForm()

	if form.validate_on_submit():

		if form.picture.data:
			#flash("Picture Data Available!!")
			picture_file = save_picture(form.picture.data)
			current_user.image_pic = picture_file

		current_user.firstname = form.firstname.data
		current_user.lastname = form.lastname.data
		current_user.email = form.email.data
		current_user.phone_number = form.phone_number.data
		db.session.commit()

		flash("Profile updated!")
		return redirect(url_for('profile'))
	elif request.method == 'GET':

		form.firstname.data = current_user.firstname
		form.lastname.data = current_user.lastname
		form.phone_number.data = current_user.phone_number
		form.email.data = current_user.email
		print(form.picture.data)
		

	posts = Post.query.filter_by(user_id= current_user.get_id()).all()
	image = url_for('static', filename='profile_images/'+ current_user.image_pic)


	return render_template("profile.html", title='Profile Page', posts=posts, image=image, form=form)




@app.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html', title='About Page')
	

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	return render_template('contact.html', title='Contact Page')

	
def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='artmanafrica.com', recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)}
	If you did not make this request then simply ignore this message and no changes will be made.
	'''
	mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('Check your email for instructions to reset your password.')
		return redirect(url_for('login'))
	return render_template('reset_request.html',title='Reset Password', form=form)



@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user = User.verify_token(token)
	if user is None:
		flash('This is an expired or invalid token.')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Password updated successfully.')
		return redirect(url_for('login'))
	return render_template('reset_token.html', form=form, title='Reset Password ')
	
@app.route('/swedish', methods=['GET', 'POST'])
@login_required
def swedish():
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	form = BookMassageForm()
	if form.validate_on_submit() and current_user.is_authenticated:
		massage = form.massage.data
		scheduled_on = form.scheduled_on.data
		user_id = current_user.id
		booking = Post(massage=massage, scheduled_on=scheduled_on, user_id= user_id)
		
		db.session.add(booking)
		db.session.commit()
		flash(f"{massage} booked on {scheduled_on}.")

	return render_template('swedish.html', form=form, title= "Swedish Massage")