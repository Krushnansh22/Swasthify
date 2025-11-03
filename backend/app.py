# File: Swasthify/backend/app.py

from flask import Flask
from flask_cors import CORS

# Import the blueprints
from policyholders_api import policyholders_bp
from policies_api import policies_bp
from providers_api import providers_bp
from claims_api import claims_bp
from auth_api import auth_bp  # <-- IMPORT THE NEW AUTH BLUEPRINT

app = Flask(__name__)
CORS(app) # Enable CORS for the entire app

@app.route('/')
def home():
    return "Swasthify API is running! Access endpoints at /api/..."

# Register the blueprints with a URL prefix
app.register_blueprint(policyholders_bp, url_prefix='/api/policyholders')
app.register_blueprint(policies_bp, url_prefix='/api/policies')
app.register_blueprint(providers_bp, url_prefix='/api/providers')
app.register_blueprint(claims_bp, url_prefix='/api/claims')
app.register_blueprint(auth_bp, url_prefix='/api/auth') # <-- REGISTER THE NEW BLUEPRINT

if __name__ == '__main__':
    # Run the Flask server
    app.run(debug=True, port=5000)