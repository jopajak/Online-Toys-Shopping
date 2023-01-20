from flask import Blueprint, render_template, session, g
from flask_login import current_user
from ..search_engine import Search

from ..forms import SearchForm, SearchFormFile

bp = Blueprint('bp_home', __name__)


@bp.route('/')
def home_get():
    form = SearchForm()
    form_file = SearchFormFile()
    g.search_engine = Search(products=[])
    return render_template('home.html', form=form, form_file=form_file, user=current_user)
