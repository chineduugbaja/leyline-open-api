from flask import Flask
from app.database import db, migrate
from app.routes import init_routes
from prometheus_flask_exporter import PrometheusMetrics

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    metrics = PrometheusMetrics(app)
    
    # Register routes
    init_routes(app)
    
    return app

# Create an instance of the Flask app
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
