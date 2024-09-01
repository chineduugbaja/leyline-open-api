import os
from datetime import datetime
from flask import jsonify
from app.utils import create_app

app = create_app()

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
