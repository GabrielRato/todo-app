
from flask import render_template
from app import app
from flask_httpauth import HTTPBasicAuth



@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
