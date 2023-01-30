from flask import Blueprint, redirect, url_for, render_template, flash, g
from flask_login import current_user

import datetime
import json

from ..forms import SearchForm, SearchFormFile, ProductSortingForm
from ..search_engine import Search

from app.database import db
from app.models import SearchInfo

ALLOWED_EXTENSIONS = {'txt'}

bp = Blueprint('bp_search', __name__)


@bp.route('/search', methods=['POST'])
def search_post():
    form = SearchForm()
    g.search_engine = Search()
    if form.validate_on_submit():
        form_data = form.data
        queries, quantities = read_queries_from_form(form_data)
        if current_user.is_authenticated:
            save_queries_to_db(queries)
        g.search_engine.search_for_products(queries, quantities)
        return redirect(url_for('bp_search.waiting_page_get', option='queries'))

    return redirect(url_for('bp_home.home_get'))


@bp.route('/search_file', methods=['POST'])
def search_file_post():
    form_file = SearchFormFile()
    g.search_engine = Search()
    if form_file.validate_on_submit():
        file_data = form_file.file.data

        if check_file(file_data):
            try:
                queries, quantities = read_queries_from_file(file_data)
            except:     # TODO specify Errors
                flash("Errors while processing file")
                return redirect(url_for('bp_home.home_get'))

            if current_user.is_authenticated:
                save_queries_to_db(queries)
            g.search_engine.search_for_products(queries, quantities)
            return redirect(url_for('bp_search.waiting_page_get', option='queries'))

        flash("Wrong filetype")
        return redirect(url_for('bp_home.home_get'))

    return redirect(url_for('bp_home.home_get'))


@bp.route('/processing/<option>')
def waiting_page_get(option):
    if option == 'queries':
        g.search_engine.check_for_searching_products()
        if g.search_engine.is_products_search_end:
            return redirect(url_for('bp_search.choose_product_get', product_id=0))
        return render_template('waiting_page.html')

    if option == 'products':
        g.search_engine.check_for_searching_offers()
        if g.search_engine.is_offers_search_end:
            return redirect(url_for('bp_search.offers_result_get'))
        return render_template('waiting_page.html')
    return render_template('404.html'), 404


@bp.route('/product/<int:product_id>')
def choose_product_get(product_id):
    try:
        list_of_products = g.search_engine.get_product_suggestions(product_id)
    except ValueError:
        return render_template('404.html'), 404
    p = []
    for product in list_of_products:
        p.append(product)
    product_length = g.search_engine.get_queries_length()
    return render_template('product_results.html', user=current_user, products=p, product_id=product_id,
                           product_length=product_length)


@bp.route('/product/<int:product_id>/<int(signed=True):option>')
def product_answer_option_get(product_id, option):
    try:
        g.search_engine.set_selected_product(product_id, option)
    except ValueError:
        return render_template('404.html'), 404
    except IndexError:
        return render_template('404.html'), 404
    return redirect(url_for('bp_search.result_get'))


@bp.route('/result')
def result_get():
    if not g.search_engine.is_products_search_end:
        return render_template('404.html'), 404
    if g.search_engine.is_option_selected_for_all():
        form = ProductSortingForm()
        result = g.search_engine.get_products_by_options()
        product_length = g.search_engine.get_queries_length()
        return render_template('search_results.html', user=current_user, products=result, form=form, product_length=product_length)
    return redirect(url_for('bp_search.choose_product_get', product_id=g.search_engine.get_first_unselected_product_id()))


@bp.route('/result', methods=['POST'])
def result_post():
    if not g.search_engine.is_products_search_end:
        return render_template('404.html'), 404
    form = ProductSortingForm()
    if form.validate_on_submit():
        if form.option.data == 'price':
            g.search_engine.set_sorting_option('price')
        if form.option.data == 'shops':
            g.search_engine.set_sorting_option('shops')

        g.search_engine.search_for_offers()
        return redirect(url_for('bp_search.waiting_page_get', option='products'))
    return redirect(url_for('bp_search.result_get'))


@bp.route('/offers_result')
def offers_result_get():

    if not g.search_engine.is_offers_search_end:
        return render_template('404.html'), 404

    if g.search_engine.get_sorting_option() == 'price':
        products = g.search_engine.get_products_by_options()
        offers = g.search_engine.get_offers_by_price()
        return render_template('offers_results_price.html',
                               user=current_user, products=products, offers=offers)

    if g.search_engine.get_sorting_option() == 'shops':
        shops_offers = g.search_engine.get_offers_by_shops()
        return render_template('offers_results_shops.html',
                               user=current_user, shops_offers=shops_offers)
    return render_template('404.html'), 404


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


def allowed_file(file) -> bool:
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
    # A function reads the contents of a text file
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


# TODO write generate file function
def generate_file(queries, quantities):
    pass


def save_queries_to_db(queries):
    db.session.add(SearchInfo(json.dumps(queries), datetime.datetime.now(), current_user.id))
    db.session.commit()
