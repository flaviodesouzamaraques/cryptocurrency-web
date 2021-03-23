import sqlite3
import bcrypt

from flask import Flask, session, redirect
from flask import render_template, request


app = Flask(__name__)
app.secret_key = b'X\xd4*\r\x1f\xd8\xc4!\xa7G\x0foj\xf8\x1d\xb9'


class User:
    def __init__(self, email, name):
        self.id = None
        self.email = email
        self.name = name
        self.password = None

    def set_password(self, password):
        '''
        This method should be used only to recreate instance from the database
        :param password: encrypted password
        '''
        self.password = password

    def set_encrypted_password(self, password):
        '''
        It should be used to set a new password, this method will encrypt the password
        using bcrypt algorithm.
        :param password: plain text password
        '''
        self.password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

    def check_password(self, password):
        '''
        Check if password matches with the encrypted password
        :param password: plain text password
        :return: boolean
        '''
        return bcrypt.checkpw(password, self.password)


class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def add(self, user):
        c = self._connection.cursor()
        c.execute('INSERT INTO users (email, name, password) VALUES (?, ?, ?)',
                  (user.email, user.name, user.password))
        c.close()

    def find_by_email(self, email):
        c = self._connection.cursor()
        c.execute(f"SELECT id, name, email, password FROM users WHERE email = '{email}'")
        r = c.fetchone()
        user = User(name=r[1], email=r[2])
        user.set_password(r[3])
        return user


@app.route("/")
def home():
    if 'user_email' in session:
        connection = sqlite3.connect('local.db')
        user_repository = UserRepository(connection)
        user = user_repository.find_by_email(email=session['user_email'])
        connection.close()
        return render_template('home.html', name=user.name)
    return render_template('signin.html', messages=['You must be logged in to access the requested page'])


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')

    elif request.method == 'POST':
        connection = sqlite3.connect('local.db')
        user_repository = UserRepository(connection)
        user = user_repository.find_by_email(email=request.form.get('email'))
        connection.close()
        if user.check_password(request.form.get('password').encode('UTF-8')):
            session['user_email'] = user.email
            return redirect('/')
        else:
            return render_template('signin.html',messages=['invalid password'])


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    connection = sqlite3.connect('local.db')
    user_repository = UserRepository(connection)
    new_user = User(name=request.form.get('name'),
                    email=request.form.get('email'))
    new_user.set_encrypted_password(request.form.get('password'))
    user_repository.add(new_user)
    connection.commit()
    connection.close()

    return render_template('signin.html', messages=['User has been saved'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)