from flask import Blueprint, render_template


from ..forms import RegistrationForm, LoginForm


bp = Blueprint('bp_auth', __name__)


@bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    form=LoginForm()
    return render_template('login.html', form=form)
