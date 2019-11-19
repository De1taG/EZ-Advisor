from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#this program defines what symbols the EZAdvisor package is resolving


#create an app object
app = Flask(__name__)

app.config['SECRET_KEY'] = '99cc3d4722f75100d23302806c98e61'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


#create the database object
db = SQLAlchemy(app)

engine = create_engine('sqlite:///site.db')

Session = sessionmaker(bind=engine)

session = Session()

#create the login sub system
login = LoginManager(app)

# If a user who is not logged in tries to view a protected page, 
# Flask-Login will automatically redirect the user to the login form
login.login_view = 'login'

from ezadvisor import routes, data