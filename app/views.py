
from flask import render_template, redirect, request, abort, url_for
from app import app, db
from flask_httpauth import HTTPBasicAuth
from .forms import LoginForm, SignupForm
from flask_login import login_required, login_user, current_user, LoginManager, logout_user
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
from js_api import new_task
from models import User, Post

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        nickname = form.nickname.data
        password = form.password.data

        user = User.query.filter(
                                User.nickname == nickname,
                                ((User.active.is_(None))|(User.active != False)),
                                ).first()
        
        if( verify_password(nickname, password) ):
            #loggin the current user queried by alchemy above
            login_user(user)
            return redirect('/user/'+form.nickname.data)
        else:
            return redirect(url_for('login'))

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
@app.route('/user/<nickname>')
#@auth.login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    post_user = Post.query.filter(Post.user_id == user.id).with_entities(Post.body)
    list_post = []
    for post in post_user:
        list_post.append(str(post.body))
    print list_post
    return render_template('user_page.html', user = user.nickname
                            , posts = list_post)



@auth.verify_password
def verify_password(nickname, password):
    user = User.query.filter_by(nickname = nickname).first()
    if not user or not user.verify_password(password):
        return False
#    g.user = user
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
