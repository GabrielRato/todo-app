
from flask import render_template, redirect, request, abort, url_for, flash
from app import app, db
from .forms import LoginForm, SignupForm
from flask_login import login_required, login_user, current_user, logout_user
from js_api import new_task
from models import User, Post

@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")


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
        
        if( user and user.verify_password(password) ):
            #loggin the current user queried by alchemy above
            if (form.remember_me.data):
                login_user(user, remember= True)
            else:
                login_user(user)
            return redirect('/user')
        else:
            flash('User or password is wrong')
            return redirect(url_for('login'))

    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        nickname = form.nickname.data
        repeat_pwd = form.repeat_pwd.data
        password = form.password.data
        email = form.email.data

        if nickname is None or password is None:
            abort(400) # missing arguments

        if User.query.filter_by(nickname = nickname).first() is not None:
            abort(400) # existing user

        if repeat_pwd != password:
            flash('Senhas diferem','error')

        else:
            user = User(nickname = nickname, email = email, pwd = password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('signup.html',
                           title='Sign In',
                           form=form)
@app.route('/user')
@login_required
def user():
    if current_user.is_authenticated:
        user = User.query.filter_by(nickname=current_user.nickname).first()
        post_user = Post.query.filter(Post.user_id == user.id).with_entities(Post.body)
        list_post = []
        for post in post_user:
            list_post.append(str(post.body))
        print list_post
        return render_template('user_page.html', user = user.nickname
                                , posts = list_post)

    else:
        return redirect(url_for('index'))


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
