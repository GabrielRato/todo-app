from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from flask_bootstrap import Bootstrap


#creates the application object
app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')
db = SQLAlchemy(app)
#prevent circular import error
from app import views, models
