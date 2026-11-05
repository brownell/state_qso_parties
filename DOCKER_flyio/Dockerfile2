# Texas QSO Party Web Application - Dockerfile
FROM python:3.11-slim


# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories (will be overridden by volume mounts in production)
RUN mkdir -p /data/batch_input \
    /data/database \
    /data/final_reports 

# Create non-root user for running the app
RUN useradd -m -u 1000 txqp && \
    chown -R txqp:txqp /app /data

# Switch to non-root user
USER txqp

# Expose port
EXPOSE 5000

# Environment variables (can be overridden)
ENV FLASK_APP=web.py \
    PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "web:app"]
