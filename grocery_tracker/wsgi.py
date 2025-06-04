# This file is the entry point for the WSGI server (e.g., Gunicorn).
# It imports the Flask application instance.

import sys
import os

# Add the project directory to the Python path
# This ensures that 'app' can be imported
project_home = os.path.abspath(os.path.dirname(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the Flask app instance from your app.py file
from app import app as application

# If you were using a specific configuration for production,
# you might load it here or ensure app.py does it.

if __name__ == "__main__":
    # This part is for local testing of this wsgi file,
    # though gunicorn would typically run this.
    # For example, you could run: gunicorn --bind 0.0.0.0:8000 wsgi:application
    print("To run this WSGI app with Gunicorn (for example):")
    print("gunicorn --bind 0.0.0.0:8000 wsgi:application")
    # from werkzeug.serving import run_simple
    # run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True)
