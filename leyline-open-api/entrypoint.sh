#!/bin/sh

# Run database migrations
flask db upgrade

# Start the Flask application
exec gunicorn -w 4 -b 0.0.0.0:3000 app.main:app
