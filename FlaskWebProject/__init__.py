"""
The flask application package.
"""

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
import os

# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'THIS IS AN INSECURE SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'sqlite:///basic_app.sqlite')
    CSRF_ENABLED = True

    USER_ENABLE_CONFIRM_EMAIL = False


    # Flask-User settings
    USER_APP_NAME        = "AppName"                # Used by email templates

# Setup Flask app and app.config
app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

# Initialize Flask extensions
db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy
mail = Mail(app)                                # Initialize Flask-Mail

# Define the User data model. Make sure to add flask.ext.user UserMixin !!!
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)

	# User authentication information
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False, server_default='')
	reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

	# User email information
	email = db.Column(db.String(255), nullable=False, unique=True)
	confirmed_at = db.Column(db.DateTime())

	# User information
	active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
	first_name = db.Column(db.String(100), nullable=False, server_default='')
	last_name = db.Column(db.String(100), nullable=False, server_default='')

# Create all database tables
db.create_all()

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User

import FlaskWebProject.views
