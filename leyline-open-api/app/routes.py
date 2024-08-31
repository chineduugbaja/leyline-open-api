from flask import Blueprint, request, jsonify
from app.models import QueryLog
from app.database import db
from app.utils import validate_ipv4
from sqlalchemy import desc
import socket

def init_routes(app):
    api = Blueprint('api', __name__)

    @api.route('/v1/tools/lookup', methods=['GET'])
    def lookup_domain():
        domain = request.args.get('domain')

        if not domain:
            return jsonify({"message": "Domain parameter is required"}), 400
            
        try:
            ipv4_addresses = socket.gethostbyname_ex(domain)[2]
        except socket.gaierror:
            return jsonify({"message": "Invalid domain"}), 400

        ipv4_addresses = [ip for ip in ipv4_addresses if validate_ipv4(ip)]
        
        query_log = QueryLog(domain=domain, result=",".join(ipv4_addresses))
        db.session.add(query_log)
        db.session.commit()

        response = {
            "domain": domain,
            "addresses": [{"ip": ip, "queryID": query_log.id} for ip in ipv4_addresses]
        }

        return jsonify(response)

    @api.route('/v1/tools/validate', methods=['POST'])
    def validate_ip():
        data = request.json
        ip = data.get('ip')

        if validate_ipv4(ip):
            return jsonify({"status": True})
        else:
            return jsonify({"status": False}), 400

    @api.route('/v1/history', methods=['GET'])
    def queries_history():
        query_logs = QueryLog.query.order_by(desc(QueryLog.timestamp)).limit(20).all()
        response = [
            {
                "queryID": log.id,
                "domain": log.domain,
                "addresses": [{"ip": addr} for addr in log.result.split(",")],
                "created_time": int(log.timestamp.timestamp())
            } for log in query_logs
        ]
        return jsonify(response)

    app.register_blueprint(api)
