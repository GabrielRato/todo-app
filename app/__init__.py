from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#creates the application object
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
#prevent circular import error
from app import views, models
