
FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    PYTHONPATH=/app

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR $APP_HOME


COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY . .


RUN chown -R appuser:appuser $APP_HOME


USER appuser


EXPOSE 3000

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh
# RUN chmod 755 /entrypoint.sh

# Use the entrypoint script to start the app
ENTRYPOINT ["/entrypoint.sh"]

# CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:3000", "--access-logfile=-", "--error-logfile=-", "--log-level=info", "app.main:app"]
