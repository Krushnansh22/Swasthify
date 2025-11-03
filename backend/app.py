# File: Swasthify/backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import db
import psycopg2
from psycopg2 import extras

app = Flask(__name__)
# CORS is crucial! It allows your frontend (on a different domain)
# to make API requests to this backend.
CORS(app) 

@app.route('/')
def home():
    return "Swasthify API is running!"

# --- API ENDPOINT 1: GET ALL POLICYHOLDERS ---
@app.route('/api/policyholders', methods=['GET'])
def get_policyholders():
    conn = None
    try:
        conn = db.get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = db.get_dict_cursor(conn)
        
        cursor.execute("SELECT * FROM PolicyHolders ORDER BY PolicyHolderID DESC")
        policyholders_rows = cursor.fetchall()
        
        cursor.close()
        
        # --- THIS IS THE CRITICAL FIX ---
        # Convert the list of 'DictRow' objects into a standard list of dicts.
        # This guarantees the JSON output has the keys: 'policyholderid', 'firstname', etc.
        policyholders_list = []
        for row in policyholders_rows:
            policyholders_list.append(dict(row))
        # ---------------------------------
            
        return jsonify(policyholders_list), 200 # Send the new list

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching policyholders: {error}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

# --- API ENDPOINT 2: CREATE A NEW POLICYHOLDER ---
@app.route('/api/policyholders', methods=['POST'])
def create_policyholder():
    conn = None
    try:
        data = request.json
        
        # Basic validation
        if not data or 'FirstName' not in data or 'Email' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        conn = db.get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        
        query = """
            INSERT INTO PolicyHolders (FirstName, LastName, DateOfBirth, Address, PhoneNumber, Email)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING PolicyHolderID;
        """
        cursor.execute(query, (
            data['FirstName'],
            data.get('LastName'),
            data.get('DateOfBirth'),
            data.get('Address'),
            data.get('PhoneNumber'),
            data['Email']
        ))
        
        new_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        
        return jsonify({"message": "Policyholder created", "PolicyHolderID": new_id}), 201

    except (Exception, psycopg2.Error) as error:
        print(f"Error creating policyholder: {error}")
        # Handle specific errors, e.g., unique constraint
        if "unique constraint" in str(error):
            return jsonify({"error": "Email or Phone Number already exists."}), 409
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

# Add other endpoints for Policies, Claims, Providers here...

if __name__ == '__main__':
    # Runs the Flask server
    app.run(debug=True, port=5000)