from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from app.database import db, migrate
from app.routes import init_routes


def create_app():
    app = Flask(__name__)
    # Load configuration
    app.config.from_object('app.config.Config')
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    # pylint: disable-next=unused-variable
    metrics = PrometheusMetrics(app)
    # Register routes
    init_routes(app)
    return app
