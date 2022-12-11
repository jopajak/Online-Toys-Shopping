from flask import Blueprint, render_template, redirect, url_for, flash, Markup, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from ..forms import RegistrationForm, LoginForm
from ..models import User
from ..app import db
from ..email import send_email
from ..token import generate_confirmation_token, confirm_token


bp = Blueprint('bp_auth', __name__)


@bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash(Markup(f'Email address already exists. Go to <a href="{url_for("bp_auth.login")}">login page</a>.'),
                  'error')
            return redirect(url_for('bp_auth.register'))

        new_user = User(email=email,
                        pw_hash=generate_password_hash(password, method='sha256', salt_length=8)
                        )

        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for('bp_auth.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(new_user.email, subject, html)

        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created you can now log in')
        return redirect(url_for('bp_auth.login'))

    return render_template('register.html', form=form)


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

    return render_template('login.html', form=form)


@bp.route('/logout')
def logout_get():
    logout_user()
    flash("You've been successfully logged out.")
    return redirect(url_for('bp_auth.login'))


@bp.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('bp_auth.login'))
    return render_template('unconfirmed.html')


@bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        session.pop('_flashes', None)
        flash('The confirmation link is invalid or has expired.', 'error')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        session.pop('_flashes', None)
        flash('Account already confirmed. Please login.', 'info')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        session.pop('_flashes', None)
        flash('You have confirmed your account. Thanks!', 'info')
    return redirect(url_for('bp_auth.login'))


@bp.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('bp_auth.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)

    session.pop('_flashes', None)
    flash('A new confirmation email has been sent.', 'info')
    return redirect(url_for('bp_auth.unconfirmed'))
