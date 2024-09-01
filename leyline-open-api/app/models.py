from datetime import datetime
from app.database import db

# pylint: disable-next=too-few-public-methods
class QueryLog(db.Model):
    """
    Model representing a log entry for DNS queries.

    Attributes:
        id (int): The primary key for the log entry.
        query (str): The DNS query string.
        response (str): The response for the DNS query.
        timestamp (datetime): The time when the query was made.
    """
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(1024), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
