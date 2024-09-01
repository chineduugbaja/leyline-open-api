from flask import Blueprint, request, jsonify
from app.models import QueryLog
from app.database import db
from app.utils import validate_ipv4
from sqlalchemy import desc
import socket
import re

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

def init_routes(app):
    api = Blueprint('api', __name__)

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

        if validate_ipv4(ip):
            return jsonify({"status": True}), HTTP_OK
        else:
            return jsonify({"status": False}), HTTP_BAD_REQUEST

    @api.route('/v1/history', methods=['GET'])
    def queries_history():
        try:
            query_logs = QueryLog.query.order_by(desc(QueryLog.timestamp)).limit(20).all()
        except Exception as e:
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