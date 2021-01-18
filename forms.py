from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length, DataRequired

class LoginForm(FlaskForm):
    name = StringField("Name", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])

class SignUpForm(FlaskForm):
    name = StringField("Name", [validators.DataRequired()])
    surname = StringField("Surname", [validators.DataRequired()])
    email = StringField("Email", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    system_role = SelectField('Status', choices=[('Select one','Select one'),('user','user'), ('admin','admin')])
    event_quota = IntegerField('Event quota', validators=[DataRequired()])

