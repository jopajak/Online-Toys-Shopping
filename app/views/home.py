from flask import Blueprint, render_template, request


bp = Blueprint('bp_home', __name__)

@bp.route('/')
def home_get():
    return render_template('home.html')


@bp.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text