import sqlite3
import bcrypt

from flask import Flask, session, redirect
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b'X\xd4*\r\x1f\xd8\xc4!\xa7G\x0foj\xf8\x1d\xb9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    password = db.Column(db.String)


class CryptocurrenceQuotes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    symbol = db.Column(db.String)
    price_currency = db.Column(db.String)
    price_amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)


@app.route("/")
def home():
    if 'user_email' in session:
        user = User.query.filter_by(email=session['user_email']).first()
        return render_template('home.html', name=user.name)
    return render_template('signin.html', messages=['You must be logged in to access the requested page'])


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')

    elif request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is not None and check_password_hash(user.password, request.form.get('password')):
            session['user_email'] = user.email
            return redirect('/')
        else:
            return render_template('signin.html',messages=['invalid credentials'])


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    new_user = User(name=request.form.get('name'),
                    email=request.form.get('email'))
    new_user.password=generate_password_hash(request.form.get('password'),method='sha256')
    db.session.add(new_user)
    db.session.commit()


    return render_template('signin.html', messages=['User has been saved'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)