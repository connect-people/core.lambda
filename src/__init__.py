from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from src.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)
    CORS(app)

    with app.app_context():
        db.init_app(app)
        register_blueprints(app)

    @app.route("/", methods=["GET"])
    def root():
        return "ok", 200

    return app


def register_blueprints(app):
    from src.routes import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/v1")
