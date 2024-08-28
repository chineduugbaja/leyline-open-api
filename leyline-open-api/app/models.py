from app.database import db
from datetime import datetime

class QueryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(1024), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
