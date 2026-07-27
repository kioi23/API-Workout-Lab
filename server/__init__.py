from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from server import models  # noqa: F401  (registers models with SQLAlchemy)

    from server.routes import bp
    app.register_blueprint(bp)

    return app