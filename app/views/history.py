from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.decorators import check_confirmed
from app.models import SearchInfo

import json

bp = Blueprint('bp_history', __name__)


@bp.route('/history')
@login_required
@check_confirmed
def history_get():
    historical_queries = SearchInfo.query\
        .filter_by(user_id=current_user.id)\
        .order_by(SearchInfo.date.desc())\
        .all()
    search_infos = {}
    for queries in historical_queries:
        search_infos[str(queries.date)] = json.loads(queries.phrase)

    return render_template('history.html',  user=current_user, search_infos=search_infos)



