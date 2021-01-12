from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    passowrd = StringField("Password", validators=[DataRequired()])
    confirm_password = StringField("Confirm Password", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    passowrd = StringField("Password", validators=[DataRequired()])
    remeber_me = BooleanField("Remember Me")
    submit = SubmitField("Login")