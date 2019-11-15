from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#this program defines what symbols the EZAdvisor package is resolving

#create an app object
app = Flask(__name__)

app.config['SECRET_KEY'] = '99cc3d4722f75100d23302806c98e61'

#create the database object
db = SQLAlchemy(app)

#create the login sub system
login = LoginManager(app)

#log in only view 
login.login_view = 'login'

from ezadvisor import routes, data