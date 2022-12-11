from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.decorators import check_confirmed


bp = Blueprint('bp_history', __name__)


@bp.route('/history')
@login_required
@check_confirmed
def history_get():
    return render_template('history.html')
