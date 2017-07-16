from flask import Flask

#creates the application object
app = Flask(__name__)
#prevent circular import error
from app import views
