from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

""" 
This is the main application module
"""

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    """ Initialize the core app """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    # Initialize plugins
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        # routes
        from .main import main_routes
        from .api import api_routes

        # registering blueprints
        app.register_blueprint(api_routes.api_bp)
        app.register_blueprint(main_routes.main_bp)

        return app
