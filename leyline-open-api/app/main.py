import os
from datetime import datetime
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from app.routes import init_routes
from app.database import db, migrate



app = Flask(__name__)
app.config.from_object('app.config.Config')

db.init_app(app)
migrate.init_app(app, db)
metrics = PrometheusMetrics(app)

init_routes(app)

@app.route('/')
def query_status():
    response = {
        "version": "0.1.0",
        "date": int(datetime.now().timestamp()),
        "kubernetes": os.getenv('KUBERNETES_SERVICE_HOST') is not None
    }
    return jsonify(response)

@app.route('/health')
def query_health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
