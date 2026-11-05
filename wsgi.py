"""
WSGI entry point for Gunicorn

This file allows Gunicorn to properly load the Flask application.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the Flask app
from app import app

# This is what Gunicorn will use
if __name__ == "__main__":
    app.run()