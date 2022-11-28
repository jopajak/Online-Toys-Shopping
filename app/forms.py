from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo


class SearchForm(FlaskForm):
    first_query = StringField('first_query', validators=[InputRequired(message='This field is required.')])
    submit = SubmitField('Search', id='searchButton')


class RegistrationForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.')])
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.')],
                             id='inputPassword')
    confirm_password = PasswordField('Confirm password',
                                     validators=[InputRequired(message='Password field is required.'),
                                                 EqualTo('password')], id='inputPasswordConfirm')
    submit = SubmitField('Register', id='submitButton')

