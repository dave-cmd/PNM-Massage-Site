import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or "kanjurus"
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///"+ os.path.join(base_dir, 'massage.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	ADMINISTRATOR_EMAIL = "kanjurus8@gmail.com"
	"""
	MAIL_SERVER = os.environ.get('MAIL_SERVER') 
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 1)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	"""
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'artmanafrica@gmail.com'
	MAIL_PASSWORD = 'mboco@123'
	ADMINS = ['devphase254@gmail.com', 'kanjurus8@gmail.com', 'kanjurus30@gmail.com']


