from flask import Blueprint, render_template, request

from ..forms import SearchForm

bp = Blueprint('bp_home', __name__)

@bp.route('/')
def home_get():
    form=SearchForm()
    return render_template('home.html', form=form)


@bp.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text