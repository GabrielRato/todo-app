from flask import render_template, redirect, request, abort, jsonify
from app import app, db
from flask_httpauth import HTTPBasicAuth
from .forms import LoginForm, SignupForm

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from models import User, Post
import json


@app.route('/oi')
def tst():
    print 'oi'
    return jsonify({"data":1})

@app.route('/add_new_task', methods = ['POST'])
def new_task():

    data = json.loads(request.get_data())
    print data
    return jsonify({"data":1})
