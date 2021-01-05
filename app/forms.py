from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, StringField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from flask_login import current_user

from app.models import User, Post

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	firstname = StringField('Firstname', validators=[DataRequired()])
	lastname = StringField('Lastname', validators=[DataRequired()])
	phone_number = IntegerField('Phone Number', validators=[DataRequired()])
	email = EmailField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit  = SubmitField('Register')

	def validate_user_email(self,email):
		user = User.query.filter_by(email=form.data).first()

		if user is not None:
			raise ValidationError("Use a different email address or login")


class UpdateForm(FlaskForm):
	firstname = StringField('Firstname', validators=[DataRequired()])
	lastname = StringField('Lastname', validators=[DataRequired()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	phone_number = IntegerField('Phone Number', validators=[DataRequired()])
	email = EmailField('Email', validators=[DataRequired(), Email()])
	submit  = SubmitField('Update')

	def validate_user_email(self,email):

		if email.data != current_user.email:
			user = User.query.filter_by(email=form.data).first()

			if user is not None:
				raise ValidationError("This email is taken, use a different one.")


class RequestResetForm(FlaskForm):
	email = EmailField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('An account does not exist with that email. Resgister first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class BookMassageForm(FlaskForm):
	massage = SelectField('Massage Selection', validators=[DataRequired()], choices=[('Swedish Massage', 'SWEDISH MASSAGE'), ('Sports Massage', 'SPORTS MASSAGE'), ('Trigger Point Massage', 'TRIGGER POINT MASSAGE'), ('Deep Tissue Massage', 'DEEP TISSUE MASSAGE'), ('Reflexology Massage','REFLEXOLOGY MASSAGE'), ('Shiatsu Massage','SHIATSU MASSAGE'), ('Thai Massage', 'THAI MASSAGE'), ('Prenatal Massage', 'PRENATAL MASSAGE'),('Couples Massage','COUPLES MASSAGE'), ('Chair Massage', 'CHAIR MASSAGE')])
	scheduled_on = DateField('Scheduled_on', format='%Y-%m-%d', validators=[DataRequired()])
	submit = SubmitField('Book Now') 






