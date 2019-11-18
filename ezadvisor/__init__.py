from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

#this program defines what symbols the EZAdvisor package is resolving

#create an app object
app = Flask(__name__)

#sets up the configuration for the app
app.config.from_object(Config)

#create the database object
db = SQLAlchemy(app)

#create the login sub system
login = LoginManager(app)

# If a user who is not logged in tries to view a protected page, 
# Flask-Login will automatically redirect the user to the login form
login.login_view = 'login'

from ezadvisor import routes, data