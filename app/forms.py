from flask_wtf import FlaskForm as Form
from wtforms import StringField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired, EqualTo



#FLASK-WTF represent forms in views as classes and defines the fields in forms
#as variables
class LoginForm(Form):
    nickname = StringField('Nickename', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class SignupForm(Form):
    nickname = StringField('Nickename', validators=[DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('repeat_pwd', message = 'Passwords must match')
    ])
    repeat_pwd = PasswordField('Repeat Password')
    email = StringField('Email', validators=[DataRequired()])


