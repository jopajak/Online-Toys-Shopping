from flask import Blueprint, render_template
from flask_login import current_user

from ..forms import SearchForm, SearchFormFile

bp = Blueprint('bp_home', __name__)


@bp.route('/')
def home_get():
    form = SearchForm()
    form_file = SearchFormFile()
    return render_template('home.html', form=form, form_file=form_file, user=current_user)
