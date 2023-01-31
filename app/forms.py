from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField
from wtforms.validators import InputRequired, EqualTo, Optional, Length
from flask_wtf.file import FileField, FileRequired
from wtforms.widgets import NumberInput


class SearchForm(FlaskForm):
    query1 = StringField('1st item', validators=[InputRequired(message='This field is required.'), Length(max=90)],
                         id='item1')
    query2 = StringField('2nd item', id='item2', validators=[Length(max=90)])
    query3 = StringField('3rd item', id='item3', validators=[Length(max=90)])
    query4 = StringField('4th item', id='item4', validators=[Length(max=90)])
    query5 = StringField('5th item', id='item5', validators=[Length(max=90)])
    query6 = StringField('6th item', id='item6', validators=[Length(max=90)])
    query7 = StringField('7th item', id='item7', validators=[Length(max=90)])
    query8 = StringField('8th item', id='item8', validators=[Length(max=90)])
    query9 = StringField('9th item', id='item9', validators=[Length(max=90)])
    query10 = StringField('10th item', id='item10', validators=[Length(max=90)])

    amount1 = IntegerField('Amount', widget=NumberInput(min=1, step=1), default=1)
    amount2 = IntegerField('Amount', widget=NumberInput(min=1, step=1), default=1)
    amount3 = IntegerField('Amount', widget=NumberInput(min=1, step=1), default=1)
    amount4 = IntegerField('Amount', widget=NumberInput(min=1, step=1), default=1)
    amount5 = IntegerField('Amount', widget=NumberInput(min=1, step=1), default=1)
    amount6 = IntegerField('Amount', widget=NumberInput(min=1, step=1), default=1)
    amount7 = IntegerField('Amount', widget=NumberInput(min=1, step=1), default=1)
    amount8 = IntegerField('Amount', widget=NumberInput(min=1, step=1), default=1)
    amount9 = IntegerField('Amount', widget=NumberInput(min=1, step=1), default=1)
    amount10 = IntegerField('Amount', widget=NumberInput(min=1, step=1), default=1)

    platform = RadioField('Platform', choices=[('Ceneo', 'Ceneo'), ('Allegro', 'Allegro (not available)'),
                                               ('C&A', 'Ceneo&Allegro (not available)')], default='Ceneo')
    price_min = IntegerField('Price from', widget=NumberInput(min=0, step=1), render_kw={"placeholder": "PLN"},
                             validators=[Optional()])
    price_max = IntegerField('Price to', widget=NumberInput(min=0, step=1), render_kw={"placeholder": "PLN"},
                             validators=[Optional()])
    stores_max = IntegerField('Maximum number of stores to buy from', widget=NumberInput(min=0, step=1),
                              validators=[Optional()])
    submit = SubmitField('Search', id='searchButton')


class SearchFormFile(FlaskForm):
    file = FileField('Shopping list', name="file", validators=[FileRequired()])

    # filters
    platform_file = RadioField('Platform', choices=[('Ceneo', 'Ceneo'), ('Allegro', 'Allegro (not available)'),
                                                    ('C&A', 'Ceneo&Allegro (not available)')], default='Ceneo')
    price_min = IntegerField('Price from', widget=NumberInput(min=0, step=1), render_kw={"placeholder": "PLN"},
                             validators=[Optional()])
    price_max = IntegerField('Price to', widget=NumberInput(min=0, step=1), render_kw={"placeholder": "PLN"},
                             validators=[Optional()])
    stores_max = IntegerField('Maximum number of stores to buy from', widget=NumberInput(min=0, step=1),
                              validators=[Optional()])
    submit = SubmitField('Search', id='searchButton')


class ProductSortingForm(FlaskForm):
    option = RadioField('Sort by:', choices=[('price', 'Price'), ('shops', 'Number of shops')], default='price')
    submit = SubmitField('Search', id='submitButton')


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
