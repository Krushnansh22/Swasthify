# File: Swasthify/backend/auth_api.py

from flask import Blueprint, request, jsonify
import db
import psycopg2

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    login_credential = data.get('credential') # This can be email or phone

    if not login_credential:
        return jsonify({"error": "Email or Phone Number is required"}), 400

    conn = None
    try:
        conn = db.get_db_connection()
        cursor = db.get_dict_cursor(conn)

        # 1. Check if Admin (hardcoded)
        if login_credential == 'admin':
            return jsonify({
                "message": "Admin login successful",
                "role": "admin",
                "name": "Admin User"
            }), 200

        # 2. Check if Patient (by Email)
        cursor.execute("SELECT PolicyHolderID, FirstName, LastName FROM PolicyHolders WHERE Email = %s", (login_credential,))
        patient = cursor.fetchone()
        if patient:
            return jsonify({
                "message": "Patient login successful",
                "role": "patient",
                "id": patient['policyholderid'],
                "name": f"{patient['firstname']} {patient['lastname']}"
            }), 200

        # 3. Check if Provider (by Phone Number)
        cursor.execute("SELECT ProviderID, ProviderName FROM Providers WHERE ContactNumber = %s", (login_credential,))
        provider = cursor.fetchone()
        if provider:
            return jsonify({
                "message": "Provider login successful",
                "role": "provider",
                "id": provider['providerid'],
                "name": provider['providername']
            }), 200
        
        # 4. If no user found
        return jsonify({"error": "Invalid credentials"}), 404

    except (Exception, psycopg2.Error) as error:
        print(f"Login error: {error}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()