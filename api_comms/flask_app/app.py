import json
import requests
from flask import Flask, request
from flask import redirect, url_for, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xe0\x8d?8z\xdd\x87i}\xfc\xaa\x91\x8f\n1\x1a\xe4\xb3\xa7\xbd5\xf8\x96\xdd'


@app.route('/')
def main_page():
    return render_template('mainpage.html', title='Main Page')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            error = "Passwords do not match!"
            return render_template('register.html', error=error, title='Register')

        # send to the server and make sure
        if username is not None and password1 is not None and password2 is not None:
            data = {username: username,
                    password1: password1}
            response = requests.get('http://localhost:8000/api/users/create_user',
                                    data=json.dumps(data), timeout=5)
            if response.status == 403:
                return render_template('register.html', title='Register')
            else:
                return redirect(url_for('login'))

    return render_template('register.html', title='Register')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username is not None and password is not None:
            data = {username: username,
                    password: password}
            response = requests.get('http://localhost:8000/api/generated_reports',
                                    data=json.dumps(data), timeout=5)
            if response.status == 403:
                return render_template('login.html', title='login')
            else:
                response = json.loads(response)
                # send data to the account display html
                return render_template('account.html', name=username, data=response)

    return render_template('login.html', title='login')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template('logout.html', title='logout')
