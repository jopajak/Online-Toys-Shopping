from flask import Blueprint, render_template, request
from flask_login import current_user

from ..forms import SearchForm, SearchFormFile

bp = Blueprint('bp_home', __name__)


@bp.route('/')
def home_get():
    form = SearchForm()
    form_file = SearchFormFile()
    return render_template('home.html', form=form, form_file=form_file, user=current_user)


@bp.route('/', methods=['POST'])
def my_form_post():
    #queries
    queries = []
    amounts = []
    if 'first_query' in request.form and request.form['first_query'] != '':
        queries.append(request.form['first_query'].upper())
        amounts.append(request.form['first_amount'])
    if 'second_query' in request.form and request.form['second_query'] != '':
        queries.append(request.form['second_query'].upper())
        amounts.append(request.form['second_amount'])
    if 'third_query' in request.form and request.form['third_query'] != '':
        queries.append(request.form['third_query'].upper())
        amounts.append(request.form['third_amount'])
    if 'fourth_query' in request.form and request.form['fourth_query'] != '':
        queries.append(request.form['fourth_query'].upper())
        amounts.append(request.form['fourth_amount'])
    if 'fifth_query' in request.form and request.form['fifth_query'] != '':
        queries.append(request.form['fifth_query'].upper())
        amounts.append(request.form['fifth_amount'])
    if 'sixth_query' in request.form and request.form['sixth_query'] != '':
        queries.append(request.form['sixth_query'].upper())
        amounts.append(request.form['sixth_amount'])
    if 'seventh_query' in request.form and request.form['seventh_query'] != '':
        queries.append(request.form['seventh_query'].upper())
        amounts.append(request.form['seventh_amount'])
    if 'eighth_query' in request.form and request.form['eighth_query'] != '':
        queries.append(request.form['eighth_query'].upper())
        amounts.append(request.form['eighth_amount'])
    if 'ninth_query' in request.form and request.form['ninth_query'] != '':
        queries.append(request.form['ninth_query'].upper())
        amounts.append(request.form['ninth_amount'])
    if 'tenth_query' in request.form and request.form['tenth_query'] != '':
        queries.append(request.form['tenth_query'].upper())
        amounts.append(request.form['tenth_amount'])

    #filters
    filters = [request.form['platform'].upper(), request.form['price_min'].upper(), request.form['price_max'].upper(),
               request.form['stores_max'].upper()]

    filename = None
    if 'file' in request.files:
        filename = request.files['file'].filename
    return render_template('search_results.html', user=current_user, queries=queries, amounts = amounts, filters=filters, filename=filename)
