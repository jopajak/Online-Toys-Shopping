from flask import Flask, flash, redirect, url_for, session, g
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_redis import FlaskRedis
import uuid
import json

from .search_engine import Search

db = SQLAlchemy()
mail = Mail()
redis_client = FlaskRedis()


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

    db.init_app(app)
    mail.init_app(app)
    redis_client.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Please log in to access this page!')
        return redirect(url_for('bp_auth.login'))

    @app.before_request
    def before_request():
        if 'search_engine' not in session:
            session['search_engine'] = vars(Search())
        key = session.get("key")
        if key:
            g.search_engine = retrieve_object_from_cache(key)
        else:
            g.search_engine = Search()
            key = generate_key()
            session["key"] = key
            store_object_in_cache(g.search_engine, key)

    def store_object_in_cache(search_engine, key):
        redis_client.set(key, json.dumps(vars(g.search_engine)))
        return key

    def retrieve_object_from_cache(key):
        data = json.loads(redis_client.get(key))
        search_engine = Search.from_json(data)
        return search_engine

    def generate_key():
        key = uuid.uuid4().hex
        return key

    @app.after_request
    def after_request(response):
        key = session.get("key")
        if key:
            store_object_in_cache(g.search_engine, key)
        return response

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

    from .views.search import bp as bp_search
    app.register_blueprint(bp_search)

    from .views.auth import bp as bp_auth
    app.register_blueprint(bp_auth)

    from .views.history import bp as bp_history
    app.register_blueprint(bp_history)

    # for localhost only
    app.run()
