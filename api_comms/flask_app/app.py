import bcrypt
from flask import Flask, request, session
from flask import render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = '\xe0\x8d?8z\xdd\x87i}\xfc\xaa\x91\x8f\n1\x1a\xe4\xb3\xa7\xbd5\xf8\x96\xdd'


@app.route('/')
def main_page():
    return render_template('mainpage.html', title='Main Page')


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template('register.html', title='Register')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username is not None and password is not None and \
                username == 'admin' and password == 'admin':
            session['logged_in'] = True
            session['username'] = request.form['username']
            return render_template('account.html', name=username)
        else:
            return render_template('login.html')

    return render_template('login.html')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template('logout.html', title='logout')
