import os
import json
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
        data = request.form

        response = requests.post(
            'http://18.217.8.244:8000/api/users/create-user/',
            data=data, timeout=15)
        if response.status_code == 201 or response.status_code == 200:
            return redirect(url_for('login'))

    return render_template('register.html', title='Register',
                           username=session.get('username'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    A function called when there's either a GET or POST request to login route received.
    For POST request, the username and password will authenticated. If the authentication successed the 
    username and password will be stored into session of the app. If not a alert message will show up.

    Returns:
        Renders login.html template which shows the login page of the app with the username stored in the session.
    """
    if request.method == 'POST':
        response = requests.get(
            'http://18.217.8.244:8000/api/users/validate-user/',
            auth=(request.form['username'], request.form['password']))

        if response.status_code == 201 or response.status_code == 200:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            return render_template('login.html', title='Login',
                                   username=session.get('username'))
        else:
            return render_template('login.html', title='Login',
                                   invalid=True)

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
                match = company['name'] == data['name'] and company['cik']
                match = match == data['cik'] and report['report_date'] == data['report_date']
                if match:
                    excel_url = report['excel_url']
                    break
        # if a url is returned, the variable 'excel_url' should not be 'Not Found'
        # therefore, redirect
        # excel_url = 'https://www.sec.gov/Archives/edgar/data/1652044/000165204421000010/Financial_Report.xlsx'
        if excel_url != 'Not Found':
            return redirect(excel_url, code=302)
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
    reports = None
    if username:
        response_generated = requests.get(
            'http://18.217.8.244:8000/api/generated-reports/',
            auth=(session.get('username'), session.get('password')), timeout=15)
        if response_generated.status_code == 200:
            reports = response_generated.json()
    return render_template('generated_report.html', title='Generated Report',
                           generated_reports=reports, username=username)


def reorganize_report(report: dict) -> list:
    """
    Reorganize a report so that it is easier to display it within a template.

    Args:
        report: A dictionary representing the generated report from the
            database.
    Returns:
        List of dictionaries representing sheets of a generated report.
    """
    sheets = []

    for sheet_name, sheet in report.items():
        new_sheet = {
            'name': sheet_name,
            'headers': ['Index', 'Name'],
            'rows': {}
        }
        for header, records in sheet.items():
            new_sheet['headers'].append(header)
            for idx, (row_name, value) in enumerate(records.items()):
                if not new_sheet['rows'].get(idx):
                    new_sheet['rows'][idx] = [idx, row_name, value]
                else:
                    new_sheet['rows'][idx].append(value)
        sheets.append(new_sheet)

    return sheets


@app.route('/generated_report/<report_id>')
def view_generated_report(report_id: int):
    """
    Args:
        report_id: A integer string representing the id of the report that
            should be viewed.

    Returns:
        Rendered HTML page that shows the generated report.
    """
    if session.get('username'):
        response = requests.get(
                f'http://18.217.8.244:8000/api/generated-reports/{report_id}',
                auth=(session.get('username'), session.get('password')),
                timeout=15
        )

        if response.status_code == 200:
            report_json = response.json()
            return render_template(
                'analysis.html',
                report_name=report_json['name'],
                report_id=report_json['id'],
                sheets=reorganize_report(json.loads(report_json['json_schema']))
            ), 200

        if response.status_code == 404:
            return render_template('not_found.html', title='Report Not '
                                                        'Found'), 404

        if response.status_code == 403:
            return render_template('forbidden.html', title='Forbidden'), 403

        return render_template('server_error.html', title='Server Error'), \
            response.status_code
    else:
        return redirect(url_for('login')), 403


@app.route('/zoom_link')
def zoom_link_company():
    # Username: secAnalyst45@outlook.com, Password: sec1nqly$T
    # login with zoom links
    # data = {'email': 'secAnalyst45@outlook.com',
    #         'password': 'sec1nqly$T'}
    # response = requests.get('https://zoom.us/signin', data=data, timeout=15)
    # if response.status_code != 200:
    #     return render_template('zoom_link.html')

    url_zoom = 'https://us05web.zoom.us/j/2112897265?pwd=SGxCZkd3OVYyNjhSaU9QZzVaWVVqdz09'
    return render_template('zoom_link.html', url_zoom=url_zoom)


@app.route('/zoom_personal')
def zoom_personal():
    #     return redirect for zoom login page
    return redirect('https://zoom.us/signin')


@app.route('/report_generation', methods=['GET', 'POST'])
def report_generation():
    """
    A function called when there's either a GET or POST request to report_generation route received.

    Returns:
        Renders report_generation.html template which shows the report_generation page of the app
        with information for requesting to create a generated report.
    """
    if request.method == 'POST':
        data = request.form.to_dict()
        if 'report_name' in data:
            return __general_information(data=data)
        else:
            return __row_selection(data=data)

    return render_template('report_generation.html', title='Report Generation', username=session.get('username'))


def __general_information(data: dict):
    """
    A private function to process the form data when a post request regarding general information is
    sent to report_generation.

    Args:
        data: A dictionary representing the request.form data.

    Returns:
        Renders template report_customization.html when the request to server is successful, otherwise renders
        report_generation.html with error message displayed.
    """
    years = request.form.getlist('years')
    data['years'] = ','.join(years)
    response = requests.post('http://18.217.8.244:8000/api/generated-reports/get-form-data/',
                             auth=(session.get('username'), session.get('password')), data=data)

    if response.status_code == 200 or response.status_code == 201:
        form_data_str = response.json()['form_data']
        form_data = json.loads(form_data_str)
        session['data'] = data
        return render_template('report_customization.html', title='Report Generation',
                               username=session.get('username'), data=data, form_data=form_data)
    else:
        print(response.reason)
        return render_template('report_generation.html', title='Report Generation',
                               invalid=True, username=session.get('username'))


def __row_selection(data: dict):
    """
        A private function to process the form data when a post request regarding row selection is
        sent to report_generation.

        Args:
            data: A dictionary representing the request.form data.

        Returns:
            Redirects to the generated_report page when the request to server is successful, otherwise renders
            report_generation.html with error message displayed.
        """
    print(data)
    form_data = {}
    for sheet in data:
        str_rows = request.form.getlist(sheet)
        rows = list(map(int, str_rows))
        form_data[sheet] = rows
    data_2 = {
        'report_name': session['data']['report_name'],
        'form_data': json.dumps(form_data),
        'type': session['data']['type']
    }
    response = requests.post('http://18.217.8.244:8000/api/generated-reports/create-report/',
                             auth=(session.get('username'), session.get('password')), data=data_2)

    if response.status_code == 200 or response.status_code == 201:
        return redirect(url_for('generated_report'))
    else:
        print(response.reason)
        return render_template('report_generation.html', title='Report Generation',
                               invalid=True, username=session.get('username'))


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
            return redirect(
                url_for('view_generated_report', report_id=report_id)
            )

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
