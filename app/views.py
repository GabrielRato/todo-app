
from flask import render_template, redirect, request, abort
from app import app, db
from flask_httpauth import HTTPBasicAuth
from .forms import LoginForm, SignupForm

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            verify_password(nickename, password)
            print (form.nickname.data, str(form.remember_me.data))
            return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        nickname = form.nickname.data
        password = form.password.data

        if nickname is None or password is None:
            print 1
            abort(400) # missing arguments

        if User.query.filter_by(nickname = nickname).first() is not None:
            print 2
            abort(400) # existing user

        user = User(nickname = nickname)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

    return render_template('signup.html',
                           title='Sign In',
                           form=form)


@auth.verify_password
def verify_password(nickename, password):
    user = User.query.filter_by(nickename = nickename).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@app.route('/api/users', methods = ['POST'])
def new_user():
    nickname = request.json.get('nickname')
    password = request.json.get('password')
    if nickname is None or password is None:
        print 1
        abort(400) # missing arguments
    if User.query.filter_by(nickname = nickname).first() is not None:
        print 2
        abort(400) # existing user
    user = User(nickname = nickname)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.nickname }), 201,{'Location':
        url_for('get_user', id = user.id, _external = True)}
