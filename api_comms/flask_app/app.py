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
    print(request.method)
    print(request.url)
    print(request.data)
    if request.method == 'POST':
        # print(len(request.data) == 0)
        if len(request.data) == 0:
            data = {"username": request.form['username'],
                    "password": request.form['password'],
                    "email": request.form['email']}
            print(data)
        else:
            data = request.data

        response = requests.post('http://18.217.8.244:8000/api/users/create_user/',
                                 data=data, timeout=5)

        if response.status_code != 200:
            return render_template('register.html', title='Register')
        elif response.status_code == 200:
            return redirect(url_for('login'))

    return render_template('register.html', title='Register')


@app.route("/login", methods=["GET", "POST"])
def login():
    print(request.method)
    print(request.url)
    print(request.data)
    if request.method == "POST":
        # print(len(request.data) == 0)
        # get input from the form
        if len(request.data) == 0:
            data = {"username": request.form['username'],
                    "password": request.form['password']}
            print(data)
        else:
            data = request.data
        response = requests.get('http://18.217.8.244:8000/api/generated-reports/',
                                data=data, timeout=5)

        print(response.status_code)
        if response.status_code != 200:
            return render_template('login.html', title='login')
        elif response.status_code == 200:
            response = json.loads(response)
            # send data to the account display html
            # return redirect(url_for('account'))
            return render_template('account.html', name=request.data['username'], data=response)

    return render_template('login.html', title='login')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template('logout.html', title='logout')
