from flask import Flask
from werkzeug.debug import DebuggedApplication

def create_app():
    # Create and configure the app
    app = Flask(__name__,
                instance_relative_config=False
                )

    # Load config from file config.py
    #app.config.from_pyfile('config.py')

    # Turn on debug mode
    app.debug = True
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

    # Register blueprints (views)
    from .views.home import bp as bp_home
    app.register_blueprint(bp_home)

    # for localhost only
    app.run()