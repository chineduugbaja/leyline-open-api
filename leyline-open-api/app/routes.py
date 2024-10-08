import socket
import re
import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from app.models import QueryLog
from app.database import db



# Constants for status codes and messages
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
DOMAIN_REQUIRED_MESSAGE = {"message": "Domain parameter is required"}
INVALID_DOMAIN_MESSAGE = {"message": "Invalid domain"}

# Helper function to validate domain names using regex
def is_valid_domain(domain):
    regex = re.compile(
        r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$"
    )
    return all(regex.match(x) for x in domain.split("."))

def validate_ipv4(ip):
    """Validate if the IP address is a valid IPv4 address."""
    pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                         r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                         r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                         r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    return pattern.match(ip) is not None

def init_routes(app):
    api = Blueprint('api', __name__)

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

    @api.route('/v1/tools/lookup', methods=['GET'])
    def lookup_domain():
        domain = request.args.get('domain')

        if not domain:
            return jsonify(DOMAIN_REQUIRED_MESSAGE), HTTP_BAD_REQUEST

        # Validate domain before DNS lookup
        if not is_valid_domain(domain):
            return jsonify(INVALID_DOMAIN_MESSAGE), HTTP_BAD_REQUEST

        try:
            ipv4_addresses = socket.gethostbyname_ex(domain)[2]
        except socket.gaierror:
            return jsonify(INVALID_DOMAIN_MESSAGE), HTTP_BAD_REQUEST

        # Filter only valid IPv4 addresses
        ipv4_addresses = [ip for ip in ipv4_addresses if validate_ipv4(ip)]

        # Log query to the database with error handling
        try:
            query_log = QueryLog(domain=domain, result=",".join(ipv4_addresses))
            db.session.add(query_log)
            db.session.commit()
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Database error", "error": str(e)}), HTTP_BAD_REQUEST

        response = {
            "domain": domain,
            "addresses": [{"ip": ip, "queryID": query_log.id} for ip in ipv4_addresses]
        }

        return jsonify(response), HTTP_OK

    @api.route('/v1/tools/validate', methods=['POST'])
    def validate_ip():
        data = request.json
        ip = data.get('ip')

        if not ip:
            return jsonify({"message": "IP address is required"}), HTTP_BAD_REQUEST

        # pylint: disable-next=no-else-return
        if validate_ipv4(ip):
            return jsonify({"status": True}), HTTP_OK
        else:
            return jsonify({"status": False}), HTTP_BAD_REQUEST

    @api.route('/v1/history', methods=['GET'])
    def queries_history():
        try:
            query_logs = QueryLog.query.order_by(desc(QueryLog.timestamp)).limit(20).all()
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            # pylint: disable-next=line-too-long
            return jsonify({"message": "Error retrieving history", "error": str(e)}), HTTP_BAD_REQUEST

        response = [
            {
                "queryID": log.id,
                "domain": log.domain,
                "addresses": [{"ip": addr} for addr in log.result.split(",")],
                "created_time": int(log.timestamp.timestamp())
            } for log in query_logs
        ]
        return jsonify(response), HTTP_OK

    app.register_blueprint(api)
