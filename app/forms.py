from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField
from wtforms.validators import InputRequired, EqualTo
from flask_wtf.file import FileField, FileRequired
from wtforms.widgets import NumberInput


class SearchForm(FlaskForm):
    first_query = StringField('1st item', validators=[InputRequired(message='This field is required.')],
                              id='firstQueryInput')
    second_query = StringField('2nd item', id='secondQueryInput')
    third_query = StringField('3rd item', id='thirdQueryInput')
    fourth_query = StringField('4th item', id='fourthQueryInput')
    fifth_query = StringField('5th item', id='fifthQueryInput')
    sixth_query = StringField('6th item', id='sixthQueryInput')
    seventh_query = StringField('7th item', id='seventhQueryInput')
    eighth_query = StringField('8th item', id='eighthQueryInput')
    ninth_query = StringField('9th item', id='ninthQueryInput')
    tenth_query = StringField('10th item', id='tenthQueryInput')

    first_amount = IntegerField('Amount', widget=NumberInput(min=0, step=1), default=1)
    second_amount = IntegerField('Amount', widget=NumberInput(min=0, step=1), default=1)
    third_amount = IntegerField('Amount', widget=NumberInput(min=0, step=1), default=1)
    fourth_amount = IntegerField('Amount', widget=NumberInput(min=0, step=1), default=1)
    fifth_amount = IntegerField('Amount', widget=NumberInput(min=0, step=1), default=1)
    sixth_amount = IntegerField('Amount', widget=NumberInput(min=0, step=1), default=1)
    seventh_amount = IntegerField('Amount', widget=NumberInput(min=0, step=1), default=1)
    eighth_amount = IntegerField('Amount', widget=NumberInput(min=0, step=1), default=1)
    ninth_amount = IntegerField('Amount', widget=NumberInput(min=0, step=1), default=1)
    tenth_amount = IntegerField('Amount', widget=NumberInput(min=0, step=1), default=1)

    # filters
    platform = RadioField('Platform', choices=[('Ceneo', 'Ceneo'), ('Allegro', 'Allegro (not available)'),
                                               ('C&A', 'Ceneo&Allegro (not available)')], default='Ceneo')
    price_min = IntegerField('Price from', widget=NumberInput(min=0, step=1), render_kw={"placeholder": "PLN"})
    price_max = IntegerField('Price to', widget=NumberInput(min=0, step=1), render_kw={"placeholder": "PLN"})
    stores_max = IntegerField('Maximum number of stores to buy from', widget=NumberInput(min=0, step=1))
    submit = SubmitField('Search', id='searchButton')


class SearchFormFile(FlaskForm):
    file = FileField('Shopping list', name="file", validators=[FileRequired()])

    # filters
    platform = RadioField('Platform', choices=[('Ceneo', 'Ceneo'), ('Allegro', 'Allegro (not available)'),
                                               ('C&A', 'Ceneo&Allegro (not available)')], default='Ceneo')
    price_min = IntegerField('Price from', widget=NumberInput(min=0, step=1), render_kw={"placeholder": "PLN"})
    price_max = IntegerField('Price to', widget=NumberInput(min=0, step=1), render_kw={"placeholder": "PLN"})
    stores_max = IntegerField('Maximum number of stores to buy from', widget=NumberInput(min=0, step=1))
    submit = SubmitField('Search', id='searchButton')


class RegistrationForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.')], id='inputEmail')
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.')],
                             id='inputPassword')
    confirm_password = PasswordField('Confirm password',
                                     validators=[InputRequired(message='Password field is required.'),
                                                 EqualTo('password')], id='inputPasswordConfirm')
    submit = SubmitField('Register', id='submitButton')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.')], id='inputEmail')
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.')],
                             id='inputPassword')
    submit = SubmitField('Log in', id='submitButton')
