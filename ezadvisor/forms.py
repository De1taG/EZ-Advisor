from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Network Username/VIP ID"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CampusForm(FlaskForm):
    aiken = SubmitField('AIKEN')
    beaufort = SubmitField('BEAUFORT')
    columbia = SubmitField('COLUMBIA')
    lancaster = SubmitField('LANCASTER')
    salkehatchie = SubmitField('SALKEHATCHIE')
    sumter = SubmitField('SUMTER')
    union = SubmitField('UNION')
    upstate = SubmitField('UPSTATE')

class TermForm(FlaskForm):
    spring = SubmitField('SPRING 2020')
    summer = SubmitField('SUMMER 2020')