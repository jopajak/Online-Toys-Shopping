from flask import Flask, flash, redirect, url_for
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


db = SQLAlchemy()


def create_app():
    # Create and configure the app
    app = Flask(__name__,
                instance_relative_config=False
                )
    Bootstrap(app)

    # Load config from file config.py
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}"
                                             f"@{app.config['DB_HOST']}/{app.config['DB_NAME']}")

    login_manager = LoginManager()
    login_manager.login_view = 'bp_auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Please log in to access this page!')
        return redirect(url_for('bp_auth.login'))

    db.init_app(app)

    from .models import User

    with app.app_context():
        db.create_all()
        db.session.commit()

    # Turn on debug mode
    app.debug = True
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

    # Register blueprints (views)
    from .views.home import bp as bp_home
    app.register_blueprint(bp_home)

    from .views.auth import bp as bp_auth
    app.register_blueprint(bp_auth)

    # for localhost only
    app.run()
