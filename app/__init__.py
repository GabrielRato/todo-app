from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, logout_user


from flask_bootstrap import Bootstrap


#creates the application object
app = Flask(__name__)
Bootstrap(app)


app.config.from_object('config')
db = SQLAlchemy(app)
#prevent circular import error
from app import views, models, js_api


#--------------Login --------------
from models import User


login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

#-------------- end login ------
