# Texas QSO Party Web Application - Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for data persistence
RUN mkdir -p /app/data \
    /app/logs/incoming \
    /app/HTML_RESULTS \
    /app/database \
    /app/temp

# Create non-root user for running the app
RUN useradd -m -u 1000 txqp && \
    chown -R txqp:txqp /app

# Switch to non-root user
USER txqp

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/app/database/txqp.db \
    UPLOAD_FOLDER=/app/logs/incoming \
    HTML_RESULTS_DIR=/app/HTML_RESULTS \
    TEMP_DIR=/app/temp

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
