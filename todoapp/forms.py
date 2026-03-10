from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class TaskForm(FlaskForm):
    done = BooleanField()
    title = StringField("Title")
    submit = SubmitField("ADD")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')