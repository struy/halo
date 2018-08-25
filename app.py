from flask import Flask
from flask import flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@app.route("/get")
def get():
    pass

@app.route("/set")
def get():
    pass



if __name__ == '__main__':
    app.debug=True
    app.secret_key = os.urandom(15)
    app.run(port=2020)
