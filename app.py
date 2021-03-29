from flask import Flask, redirect, url_for
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask_login import UserMixin


app = Flask(__name__)
app.secret_key = b'X\xd4*\r\x1f\xd8\xc4!\xa7G\x0foj\xf8\x1d\xb9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    password = db.Column(db.String)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class CryptocurrencyQuote(db.Model):
    __tablename__ = 'cryptocurrency_quotes'
    symbol = db.Column(db.String, primary_key=True)
    price_currency = db.Column(db.String, primary_key=True)
    price_amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, primary_key=True)


@app.route("/")
@login_required
def home():
    quotes = CryptocurrencyQuote.query \
                                .order_by(CryptocurrencyQuote.timestamp.desc()) \
                                .limit(10) \
                                .all()
    return render_template('home.html', name=current_user.name, quotes=quotes)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('signin'))


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')

    elif request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is not None and check_password_hash(user.password, request.form.get('password')):
            login_user(user, remember=True)
            return redirect('/')
        else:
            return render_template('signin.html', messages=['invalid credentials'])


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    new_user = User(name=request.form.get('name'),
                    email=request.form.get('email'),
                    password=generate_password_hash(request.form.get('password'), method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return render_template('signin.html', messages=['User has been saved'])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)