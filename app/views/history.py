from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.decorators import check_confirmed
from app.models import SearchInfo

bp = Blueprint('bp_history', __name__)


@bp.route('/history')
@login_required
@check_confirmed
def history_get():
    args = request.args
    take = args.get("take", default=10, type=int)
    skip = args.get("skip", default=0, type=int)
    search_infos = SearchInfo.query.filter_by(user_id=current_user.id).order_by(SearchInfo.date.desc())\
        .offset(skip).all()
    return render_template('history.html',  user=current_user, search_infos=search_infos)
