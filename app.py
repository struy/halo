from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for, jsonify, make_response
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import User, Entity
from functools import wraps
import os, json
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
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
        entries = db.session.query(Entity).filter(Entity.user_id == session['owner']).all()

    else:
        entries = None
    return render_template('index.html', entries=entries, username=session.get('username'))


@app.route('/getall')
def get_all_entities():
    entries = db.session.query(Entity).filter(Entity.user_id == session['owner']).all()
    return make_response(jsonify([i.serialize for i in entries]), 200)


@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])

        query = db.session.query(User).filter(User.username == POST_USERNAME).first()

        if check_password_hash(query.password, POST_PASSWORD):
            session['logged_in'] = True
            session['owner'] = query.id
            session['username'] = POST_USERNAME
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


@app.route("/get/<string:slug>")
@authenticate
def get(slug):
    query = db.session.query(Entity).filter(
        Entity.key.in_([slug]),
        Entity.user_id.in_([session["owner"]])).one_or_none()

    return render_template('single.html', entity=query)


@app.route("/api/get/<string:slug>", methods=['POST'])
@authenticate
def getapi(slug):
    query = db.session.query(Entity).filter(
        Entity.key.in_([slug]),
        Entity.user_id.in_([session["owner"]])).one_or_none()

    return make_response(jsonify(query.serialize), 200)


@app.route("/api/set", methods=['POST'])
@authenticate
def set():
    data = request.get_json()
    key = data['key']
    value = data['value']

    if key and value:
        query = db.session.query(Entity).filter(Entity.key == key, Entity.user_id == session['owner']).first()
        if query is not None:
            if query.value == value:
                flash('key/value yet exist')
                return json.dumps({'status': 'key/value yet exist'})
            query.value = value
            db.session.commit()
        else:
            db.session.add(Entity(key=key, value=value, user_id=session['owner']))
            db.session.commit()
            message = ('').join(("Have set ", key, "/", value))
            flash(message)
    else:
        flash('Not correct data!')
        return json.dumps({'status': 'Not correct data!'})
    return json.dumps({'status': 'OK'})


if __name__ == '__main__':
    app.debug = True
    app.secret_key = os.urandom(15)
    toolbar = DebugToolbarExtension(app)
    app.run(port=2020)
