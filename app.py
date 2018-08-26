from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import User, Entity
from functools import wraps
import os
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return "access denied (＾ｖ＾)", 404, {"Refresh": "3; url=/"}
        return f(*args, **kwargs)
    return wrapper


@app.route('/')
def index():
    if session.get('logged_in') and session['owner']:
        entries = db.session.query(Entity).filter(Entity.user_id==session['owner']).all()
    else:
        entries = None
    return render_template('index.html', entries=entries)


@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])

        query = db.session.query(User).filter(User.username.in_([POST_USERNAME])).first()

        if check_password_hash(query.password, POST_PASSWORD):
            session['logged_in'] = True
            session['owner'] = query.id
            return index()
        else:
            flash('wrong password!')
    return render_template('login.html')





@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@app.route("/get/", methods=['GET'])
@authenticate
def get():
    pass


@app.route("/set", methods=['POST'])
@authenticate
def set():
    key = request.form['key']
    value = request.form['value']
    if key and value:
        db.session.add(Entity(key=key, value=value, user_id=session['owner']))
    else:
        flash('Not correct data!')
    return index()


if __name__ == '__main__':
    app.debug = True
    app.secret_key = os.urandom(15)
    toolbar = DebugToolbarExtension(app)
    app.run(port=2020)
