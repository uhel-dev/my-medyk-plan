from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, EmailField
from wtforms.validators import DataRequired, EqualTo


class RegistrationForm(FlaskForm):
    full_name = StringField('full_name', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm-password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register-btn')



class LoginForm(FlaskForm):
    email = StringField('email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('password', [validators.DataRequired()])
    submit = SubmitField('login')
