import os
import requests
from flask import Flask, session, redirect, url_for, request, render_template

"""
A file that defines the routes for the frontend Flask application.

This file configures the routes and render templates for the UI. Calls the Django API for data retrieval and
stores the user's information in the session.

Fields:
    app: The Flask app instance
    UI_PORT: The port that this Flask app will be ran on.
"""
app = Flask(__name__, static_folder='static')
app.config[
    'SECRET_KEY'] = '\xe0\x8d?8z\xdd\x87i}\xfc\xaa\x91\x8f\n1\x1a\xe4\xb3\xa7\xbd5\xf8\x96\xdd'

UI_PORT = os.getenv('UI_PORT')


@app.route('/')
def main_page():
    """
    A function called when there's a GET request to index route received.

    Returns:
        Renders mainpage.html template which shows the homepage of the app.
    """
    return render_template('mainpage.html', title='Main Page')


@app.route('/docs')
def documentation():
    """
    A function called when there's a GET request to index route received.

    Returns:
        Renders mainpage.html template which shows the homepage of the app.
    """
    return render_template('docs/html/index.html', title='Documentation')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    A function called when there's either a GET or POST request to register route received.

    Returns:
        For GET request, renders register.html template which shows the register page of the app.
        For POST request, renders login.html template which shows the login page of the app after sending a POST
        request to the registration API.
    """
    if request.method == 'POST':
        data = request.data

        response = requests.post(
            'http://18.217.8.244:8000/api/users/create_user/',
            data=data, timeout=15)
        if response.status_code == 201 or response.status_code == 200:
            return redirect(url_for('login'))

    return render_template('register.html', title='Register',
                           username=session.get('username'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    A function called when there's either a GET or POST request to login route received.
    For POST request, the username and password will be stored into session of the app.

    Returns:
        Renders login.html template which shows the login page of the app with the username stored in the session.
    """
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']

    return render_template('login.html', title='Login',
                           username=session.get('username'))


@app.route('/logout')
def logout():
    """
    A function called when there's a GET request to login route received.
    Removes the username in the flask session.

    Returns:
        Renders logout.html template which shows the logout page of the app.
    """
    session.pop('username', None)
    return render_template('logout.html', title='Logout')


@app.route('/raw_report', methods=['GET', 'POST'])
def raw_report():
    """
    A function called when there's either a GET or POST request to raw_report route received.
    For POST request, send request to raw-reports API to retrieve the report information, and iterate over the
    reports to find the matched report. Add the url to the parameter of the rendered template.

    Returns:
        Renders raw_report.html template which shows the raw_report page of the app with information of the requested
        reports and the current username.
    """
    if request.method == 'POST':
        data = request.form
        response_raw = requests.get('http://18.217.8.244:8000/api/raw-reports/',
                                    timeout=15)

        excel_url = 'Not Found'
        if response_raw.status_code == 200:
            reports = response_raw.json()
            for report in reports:
                company = report['company']
                match = company['name'] == data['name'] and company['cik'] == \
                        data['cik'] and \
                        report['report_date'] == data['report_date']
                if match:
                    excel_url = report['excel_url']
                    break
        return render_template('raw_report.html', title='Raw Report',
                               username=session.get('username'),
                               excel_url=excel_url)

    return render_template('raw_report.html', title='Raw Report',
                           username=session.get('username'))


@app.route('/generated_report')
def generated_report():
    """
    A function called when there's either a GET request to generated_report route received.
    It sends a request to the API to retrieve the generated report information, and add the json response
    to the parameter of the rendered template.

    Returns:
        Renders generated_report.html template which shows the generated_report page of the app
        with information of the current user's generated reports and the username.
    """
    username = session.get('username')
    report = None
    if username:
        response_generated = requests.get(
            'http://18.217.8.244:8000/api/generated-reports/',
            auth=(session.get('username'), session.get('password')), timeout=15)
        if response_generated.status_code == 200:
            report = response_generated.json()
    return render_template('generated_report.html', title='Generated Report',
                           generated_report=report, username=username)


@app.route('/create_generated_report', methods=['GET', 'POST'])
def create_generated_report():
    """
    A function called when there's either a GET or POST request to create_generated_report route received.
    

    Returns:
        Renders create_generated_report.html template which shows the create_generated_report page of the app 
        with information for requesting a generated report.
    """
    if request.method == 'POST':
        data = request.form
        response_raw = requests.get('http://18.217.8.244:8000/api/generated-reports/create-report/',
                                    auth=(session.get('username'), session.get('password')), 
                                    data=data,
                                    timeout=15)

        report_id = '-1'
        if response_raw.status_code == 200:
            report_id = response_raw.json()
            
        return render_template('report_generation.html', title='Create Genrated Report',
                               username=session.get('username'),
                               report_id=report_id)

    return render_template('report_generation.html', title='Create Genrated Report2',
                               username=session.get('username'))
                            #    report_id=report_id)
    # return render_template('raw_report.html', title='Raw Report',
    #                        username=session.get('username'))

@app.route('/generated_report/analysis/<report_id>')
def analysis(report_id: str):
    """
    Returns:
        Rendered analysis.html template
    """

    username = session.get('username')

    if username:
        response = requests.post(
            f'http://18.217.8.244:8000/api/generated-reports/analysis/',
            auth=(session.get('username'), session.get('password')),
            data={"report_id": report_id},
            timeout=15)

        if response.status_code == 200:
            return render_template('analysis.html', title='Report Analysis',
                                   report=response.json(),
                                   username=username), 200

        if response.status_code == 404:
            return render_template('not_found.html', title='Report Not '
                                                           'Found'), 404

        if response.status_code == 403:
            return render_template('forbidden.html', title='Forbidden'), 403

        return render_template('server_error.html', title='Server Error'), \
               response.status_code

    # user not logged in
    return render_template('login.html', title='Login',
                           username=session.get('username')), 403


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=UI_PORT)
