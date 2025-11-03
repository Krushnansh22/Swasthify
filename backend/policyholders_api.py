# File: Swasthify/backend/policyholders_api.py

from flask import Blueprint, request, jsonify
import db
import psycopg2

# Define the blueprint
policyholders_bp = Blueprint('policyholders_bp', __name__)

# --- GET ALL POLICYHOLDERS ---
@policyholders_bp.route('/', methods=['GET'])
def get_policyholders():
    conn = None
    try:
        conn = db.get_db_connection()
        cursor = db.get_dict_cursor(conn)
        cursor.execute("SELECT * FROM PolicyHolders ORDER BY PolicyHolderID DESC")
        policyholders_rows = cursor.fetchall()
        cursor.close()
        
        policyholders_list = [dict(row) for row in policyholders_rows]
            
        return jsonify(policyholders_list), 200
    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching policyholders: {error}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

# --- CREATE A NEW POLICYHOLDER ---
@policyholders_bp.route('/', methods=['POST'])
def create_policyholder():
    conn = None
    try:
        data = request.json
        if not data or 'FirstName' not in data or 'Email' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        conn = db.get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO PolicyHolders (FirstName, LastName, DateOfBirth, Address, PhoneNumber, Email)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING PolicyHolderID;
        """
        cursor.execute(query, (
            data['FirstName'], data.get('LastName'), data.get('DateOfBirth'),
            data.get('Address'), data.get('PhoneNumber'), data['Email']
        ))
        
        new_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        
        return jsonify({"message": "Policyholder created", "PolicyHolderID": new_id}), 201
    except (Exception, psycopg2.Error) as error:
        print(f"Error creating policyholder: {error}")
        if "unique constraint" in str(error):
            return jsonify({"error": "Email or Phone Number already exists."}), 409
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

# --- We should also add GET (one), PUT, and DELETE for completeness ---

# --- GET A SINGLE POLICYHOLDER ---
@policyholders_bp.route('/<int:id>', methods=['GET'])
def get_policyholder_by_id(id):
    conn = None
    try:
        conn = db.get_db_connection()
        cursor = db.get_dict_cursor(conn)
        cursor.execute("SELECT * FROM PolicyHolders WHERE PolicyHolderID = %s", (id,))
        policyholder = cursor.fetchone()
        cursor.close()
        if policyholder:
            return jsonify(dict(policyholder)), 200
        else:
            return jsonify({"error": "Policyholder not found"}), 404
    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching policyholder: {error}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

# --- UPDATE A POLICYHOLDER ---
@policyholders_bp.route('/<int:id>', methods=['PUT'])
def update_policyholder(id):
    conn = None
    try:
        data = request.json
        conn = db.get_db_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE PolicyHolders
            SET FirstName = %s, LastName = %s, DateOfBirth = %s, 
                Address = %s, PhoneNumber = %s, Email = %s
            WHERE PolicyHolderID = %s
        """
        cursor.execute(query, (
            data['FirstName'], data.get('LastName'), data.get('DateOfBirth'),
            data.get('Address'), data.get('PhoneNumber'), data['Email'], id
        ))
        
        updated_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        
        if updated_rows == 0:
            return jsonify({"error": "Policyholder not found"}), 404
        return jsonify({"message": "Policyholder updated successfully"}), 200
    except (Exception, psycopg2.Error) as error:
        print(f"Error updating policyholder: {error}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

# --- DELETE A POLICYHOLDER ---
@policyholders_bp.route('/<int:id>', methods=['DELETE'])
def delete_policyholder(id):
    conn = None
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PolicyHolders WHERE PolicyHolderID = %s", (id,))
        deleted_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        
        if deleted_rows == 0:
            return jsonify({"error": "Policyholder not found"}), 404
        return jsonify({"message": "Policyholder deleted successfully"}), 200
    except (Exception, psycopg2.Error) as error:
        # Handle foreign key constraint error
        if "foreign key constraint" in str(error):
            return jsonify({"error": "Cannot delete: Policyholder has active dependents or enrollments."}), 409
        print(f"Error deleting policyholder: {error}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()