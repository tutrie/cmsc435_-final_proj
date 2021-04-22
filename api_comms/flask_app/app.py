import requests
from flask import Flask, request
from flask import redirect, url_for, render_template
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xe0\x8d?8z\xdd\x87i}\xfc\xaa\x91\x8f\n1\x1a\xe4\xb3\xa7\xbd5\xf8\x96\xdd'

UI_PORT = os.getenv("UI_PORT")


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
                                 data=data, timeout=15)
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

        # response_user = requests.get('http://18.217.8.244:8000/api/users/',
        #                              auth=(data["username"], data["password"]), timeout=15)

        response_generated = requests.get('http://18.217.8.244:8000/api/generated-reports/',
                                          auth=(data["username"], data["password"]), timeout=15)

        response_raw = requests.get('http://18.217.8.244:8000/api/raw-reports/',
                                    auth=(data["username"], data["password"]), timeout=15)

        if response_generated.status_code == 200 and response_raw.status_code == 200:
            return render_template('account.html', data_generated=response_generated.json(),
                                   data_raw=response_raw.json(), name=request.form['username'])

        # if response_user.status_code == 200:
        #     # how to pass response.json() to redirect url
        #     return redirect(url_for('account'))

    return render_template('login.html', title='Login')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template('logout.html', title='Logout')


@app.route('/account')
def account():
    return render_template('account.html', title='Account')


@app.route('/raw_report')
def raw_report():
    # response_raw = requests.get('http://18.217.8.244:8000/api/raw-reports/',
    #                             auth=(data["username"], data["password"]), timeout=15)
    #
    # if response_raw.status_code == 200:
    #     return render_template('raw_report.html', title='Raw Report', data=response_raw.json())

    return render_template('raw_report.html', title='Raw Report', data=request)


@app.route('/generated_report')
def generated_report():
    # response_generated = requests.get('http://18.217.8.244:8000/api/generated-reports/',
    #                                   auth=(data["username"], data["password"]), timeout=15)
    #
    # if response_generated.status_code == 200:
    #     return render_template('generated_report.html', title='Generated Report', data=response_generated.json())

    return render_template('generated_report.html', title='Generated Report')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=UI_PORT)
    
