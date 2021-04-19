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
        if len(request.data) == 0:
            data = {"username": request.form['username'],
                    "password": request.form['password'],
                    "email": request.form['email']}
        else:
            data = request.data

        response = requests.post('http://18.217.8.244:8000/api/users/create_user/',
                                 data=data, timeout=5)
        if response.status_code == 201 or response.status_code == 200:
            return redirect(url_for('login'))

    return render_template('register.html', title='Register')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if len(request.data) == 0:
            data = {"username": request.form['username'],
                    "password": request.form['password']}
        else:
            data = request.data

        response = requests.get('http://18.217.8.244:8000/api/generated-reports/',
                                auth=(data["username"], data["password"]), timeout=5)
        print(response)
        if response.status_code == 200:
            return render_template('account.html', data=response.json())

    return render_template('login.html', title='login')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template('logout.html', title='logout')

