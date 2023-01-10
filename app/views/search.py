from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user

from ..forms import SearchForm, SearchFormFile

ALLOWED_EXTENSIONS = {'txt'}

bp = Blueprint('bp_search', __name__)


@bp.route('/search', methods=['POST'])
def search_post():
    form = SearchForm()
    # return form.data
    if form.validate_on_submit():
        queries = form.data
        queries.pop('submit', None)
        queries.pop('csrf_token', None)
        items, quantities = read_items_from_form(queries)
        return render_template('search_results.html', user=current_user, queries=items, amounts=quantities, filters=[1])
    print(form.errors)

    return redirect(url_for('bp_home.home_get'))


@bp.route('/search_file', methods=['POST'])
def search_file_post():
    form_file = SearchFormFile()
    if form_file.validate_on_submit():
        file = form_file.file.data

        if check_file(file):
            try:
                items, quantities = read_items_from_file(file)
            except:     # TODO specify Errors
                flash("Errors while processing file")
                return redirect(url_for('bp_home.home_get'))

            return render_template('search_results.html', user=current_user, queries=items, amounts=quantities,
                                   filters=[1])

        flash("Wrong filetype")
        return redirect(url_for('bp_home.home_get'))

    return redirect(url_for('bp_home.home_get'))


def read_items_from_form(form):
    items = []
    quantities = []

    for i in range(10):
        query_key = f'query{i + 1}'
        amount_key = f'amount{i + 1}'
        query = form.get(query_key)
        amount = form.get(amount_key)
        if query != "":
            items.append(query)
            quantities.append(amount)

    return items, quantities


def allowed_file(file):
    return '.' in file.filename and \
           file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_file(file) -> bool:
    if file and file.filename and allowed_file(file):
        return True
    else:
        return False


def read_items_from_file(file):
    lines = file.read().decode('utf-8').split('\n')
    items = []
    quantities = []

    for line in lines:
        if line:  # check if the string is non-empty
            parts = line.split('\t')
            items.append(parts[0])
            if not any(c.isdigit() for c in parts[1]):
                quantities.append(1)
            else:
                quantities.append(int(parts[1].rstrip()))

    return items, quantities
