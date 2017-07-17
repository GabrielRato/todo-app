from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired



#FLASK-WTF represent forms in views as classes and defines the fields in forms
#as variables
class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
