from flask import Blueprint, redirect, url_for, render_template, flash, session
from flask_login import current_user
from ..search_engine import Search

from ..forms import SearchForm, SearchFormFile

ALLOWED_EXTENSIONS = {'txt'}

bp = Blueprint('bp_search', __name__)


@bp.route('/search', methods=['POST'])
def search_post():
    form = SearchForm()
    search_engine = Search.from_json(session['search_engine'])

    if form.validate_on_submit():
        form_data = form.data
        queries, quantities = read_queries_from_form(form_data)
        # TODO implement the creation of a new thread to search for offers
        search_engine.search_for_queries(queries, quantities)
        # before each return you must save the state of the object to a session variable
        session['search_engine'] = vars(search_engine)
        return redirect(url_for('bp_search.waiting_page_get'))

    # before each return you must save the state of the object to a session variable
    session['search_engine'] = vars(search_engine)
    return redirect(url_for('bp_home.home_get'))


@bp.route('/search_file', methods=['POST'])
def search_file_post():
    form_file = SearchFormFile()
    search_engine = Search.from_json(session['search_engine'])
    if form_file.validate_on_submit():
        file_data = form_file.file.data

        if check_file(file_data):
            try:
                queries, quantities = read_queries_from_file(file_data)
            except:     # TODO specify Errors
                flash("Errors while processing file")
                return redirect(url_for('bp_home.home_get'))

            search_engine.search_for_queries(queries, quantities)
            session['search_engine'] = vars(search_engine)
            return redirect(url_for('bp_search.waiting_page_get'))

        session['search_engine'] = vars(search_engine)
        flash("Wrong filetype")
        return redirect(url_for('bp_home.home_get'))

    session['search_engine'] = vars(search_engine)
    return redirect(url_for('bp_home.home_get'))


@bp.route('/processing')
def waiting_page_get():
    search_engine = Search.from_json(session['search_engine'])
    if search_engine.is_search_end:
        return redirect(url_for('bp_search.choose_product_get', product_id=0))
    return render_template('waiting_page.html')


@bp.route('/product/<int:product_id>')
def choose_product_get(product_id):
    search_engine = Search.from_json(session['search_engine'])
    print(search_engine.items_offers)
    try:
        list_of_products = search_engine.get_item_offers(product_id)
    except ValueError as e:
        flash(str(e))
        # TODO change to flask handling error 404
        # before each return you must save the state of the object to a session variable
        session['search_engine'] = vars(search_engine)
        return render_template('404.html')
    p = []
    for product in list_of_products:
        p.append(product)
    # before each return you must save the state of the object to a session variable
    session['search_engine'] = vars(search_engine)
    return render_template('search_results.html', user=current_user, products=p)


def read_queries_from_form(form_data) -> tuple[list[str], list[int]]:
    queries = []
    quantities = []

    for i in range(10):
        query_key = f'query{i + 1}'
        amount_key = f'amount{i + 1}'
        query = form_data.get(query_key)
        quantity = form_data.get(amount_key)
        if query != "":
            queries.append(query)
            quantities.append(quantity)

    return queries, quantities


def allowed_file(file):
    # A function that checks if a file is txt
    return '.' in file.filename and \
           file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_file(file) -> bool:
    # A function that checks if a file is txt or empty
    if file and file.filename and allowed_file(file):
        return True
    else:
        return False


def read_queries_from_file(file_data) -> tuple[list[str], list[int]]:
    # Function reads the contents of a text file
    lines = file_data.read().decode('utf-8').split('\n')
    queries = []
    quantities = []

    for line in lines:
        if line:  # check if the string is non-empty
            parts = line.split('\t')    # parts[0] is a query text, parts[1] is number of products in the query
            queries.append(parts[0])
            if not any(c.isdigit() for c in parts[1]):
                quantities.append(1)
            else:
                quantities.append(int(parts[1].rstrip()))

    return queries, quantities
