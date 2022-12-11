from flask import Blueprint, render_template, request
from flask_login import current_user

from ..forms import SearchForm

bp = Blueprint('bp_home', __name__)


@bp.route('/')
def home_get():
    form = SearchForm()
    return render_template('home.html', form=form, user=current_user)


@bp.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text
