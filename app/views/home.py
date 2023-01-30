import json

from flask import Blueprint, render_template, g
from flask_login import current_user, login_required
from ..search_engine import Search

from ..forms import SearchForm, SearchFormFile

from app.decorators import check_confirmed
from app.models import SearchInfo

bp = Blueprint('bp_home', __name__)


@bp.route('/')
def home_get():
    form = SearchForm()
    form_file = SearchFormFile()
    g.search_engine = Search(products=[])
    return render_template('home.html', form=form, form_file=form_file, user=current_user)


@bp.route('/history/<int:option>')
@login_required
@check_confirmed
def history_home_get(option):
    historical_queries = SearchInfo.query \
        .filter_by(user_id=current_user.id) \
        .order_by(SearchInfo.date.desc()) \
        .all()
    try:
        queries = json.loads(historical_queries[option].phrase)
    except:
        return render_template('404.html'), 404

    form_data = {}
    for i, query in enumerate(queries):
        query_key = f'query{i + 1}'
        form_data[query_key] = query

    form = SearchForm(**form_data)
    form_file = SearchFormFile()
    g.search_engine = Search(products=[])
    return render_template('home.html', form=form, form_file=form_file, user=current_user)