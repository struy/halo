from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import User, Entity

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if request.method == 'POST':
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
        else:
            flash('wrong password!')
        return index()
    else:
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


@app.route("/get")
def get():
    pass


@app.route("/set")
def set():
    pass


if __name__ == '__main__':
    app.debug = True
    app.secret_key = os.urandom(15)
    toolbar = DebugToolbarExtension(app)
    app.run(port=2020)
