# Texas QSO Party Web Application - Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    DATABASE_FILE=/data/txqp.db \
    TEMP_DIR=/app/temp

COPY . .

EXPOSE 8080
# Install system dependencies
# Install Git before pip processes the GitHub dependency.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Create non-root user for running the app
RUN useradd -m -u 1000 txqp && \
    chown -R txqp:txqp /app

# Switch to non-root user
USER txqp

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "120", "app:app"]

# to run the machine in debug mode
#CMD ["python", "-m", "http.server", "8080", "--bind", "0.0.0.0", "--directory", "/tmp"]
