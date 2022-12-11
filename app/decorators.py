from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def check_confirmed(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user.confirmed is False:
            return redirect(url_for('bp_auth.unconfirmed'))
        return f(*args, **kwargs)

    return function
