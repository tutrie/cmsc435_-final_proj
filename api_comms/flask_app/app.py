from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user
from rest_framework.authtoken.admin import User
import bcrypt
from middleware.query_engine import query_engine

from api_comms import LoginForm, RegistrationForm

users = Blueprint("users", __name__)


@users.route("/account", methods=["GET", "POST"])
# @login_required
def account():
    # display account details
    # use query engine here
    lst = {}
    query_engine.query(lst)
    return


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('something.here'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()
        # return these
        username = form.username
        password = form.password

        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is not None and bcrypt.check_password_hash(
                user.password, form.password.data):
            login_user(user)
            return redirect(url_for('users.account'))
        else:
            flash("login failed.  check credentials")
            return redirect(url_for('users.login'))

    return render_template('templates/login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
