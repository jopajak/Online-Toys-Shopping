from flask import Blueprint, render_template


from ..forms import RegistrationForm


bp = Blueprint('bp_auth', __name__)


@bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)
