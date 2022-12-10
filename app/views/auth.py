from flask import Blueprint, render_template, redirect, url_for, flash, Markup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

from ..forms import RegistrationForm, LoginForm
from ..models import User
from ..app import db


bp = Blueprint('bp_auth', __name__)


@bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash(Markup(f'Email address already exists. Go to <a class="danger-link" href="{url_for("bp_auth.login")}">login page</a>.'),
                  'error')
            return redirect(url_for('bp_auth.register'))

        new_user = User(email=email,
                        pw_hash=generate_password_hash(password, method='sha256', salt_length=8)
                        )

        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created you can now log in')
        return redirect(url_for('bp_auth.login'))

    return render_template('register.html', form=form, user=current_user)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bp_home.home_get'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.pw_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('bp_auth.login'))

        login_user(user)
        return redirect(url_for('bp_home.home_get'))

    return render_template('login.html', form=form, user=current_user)


@bp.route('/logout')
def logout_get():
    logout_user()
    flash("You've been successfully logged out.")
    return redirect(url_for('bp_auth.login'))
