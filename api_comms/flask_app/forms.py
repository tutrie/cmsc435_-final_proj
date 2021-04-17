from sqlalchemy.testing import db
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import (
    InputRequired,
    Length,
    EqualTo,
    ValidationError,
)
# from models import User
class User:
    username = db.StringField(required=True, unique=True, min_length=1, max_length=20)
    password = db.StringField(required=True, min_length=1, max_length=20)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class RegistrationForm:
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=20)]
    )
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm():
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")
