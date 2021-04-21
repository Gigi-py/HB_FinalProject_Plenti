from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    fname = StringField('username', validators=[DataRequired()])
    lname = StringField('username', validators=[DataRequired()])
    email = StringField('password', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
