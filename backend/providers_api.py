# File: Swasthify/backend/providers_api.py

from flask import Blueprint, request, jsonify
import db
import psycopg2

providers_bp = Blueprint('providers_bp', __name__)

# --- GET ALL PROVIDERS ---
@providers_bp.route('/', methods=['GET'])
def get_providers():
    conn = db.get_db_connection()
    cursor = db.get_dict_cursor(conn)
    cursor.execute("SELECT * FROM Providers ORDER BY ProviderID")
    providers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(row) for row in providers]), 200

# --- CREATE A NEW PROVIDER ---
@providers_bp.route('/', methods=['POST'])
def create_provider():
    data = request.json
    conn = db.get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO Providers (ProviderName, Address, ProviderType, ContactNumber)
        VALUES (%s, %s, %s, %s)
        RETURNING ProviderID;
    """
    cursor.execute(query, (
        data['ProviderName'], data.get('Address'),
        data.get('ProviderType'), data.get('ContactNumber')
    ))
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Provider created", "ProviderID": new_id}), 201

# --- GET A SINGLE PROVIDER ---
@providers_bp.route('/<int:id>', methods=['GET'])
def get_provider_by_id(id):
    conn = db.get_db_connection()
    cursor = db.get_dict_cursor(conn)
    cursor.execute("SELECT * FROM Providers WHERE ProviderID = %s", (id,))
    provider = cursor.fetchone()
    cursor.close()
    conn.close()
    if provider:
        return jsonify(dict(provider)), 200
    else:
        return jsonify({"error": "Provider not found"}), 404

# --- UPDATE A PROVIDER ---
@providers_bp.route('/<int:id>', methods=['PUT'])
def update_provider(id):
    data = request.json
    conn = db.get_db_connection()
    cursor = conn.cursor()
    query = """
        UPDATE Providers
        SET ProviderName = %s, Address = %s, ProviderType = %s, ContactNumber = %s
        WHERE ProviderID = %s
    """
    cursor.execute(query, (
        data['ProviderName'], data.get('Address'),
        data.get('ProviderType'), data.get('ContactNumber'), id
    ))
    updated_rows = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    if updated_rows == 0:
        return jsonify({"error": "Provider not found"}), 404
    return jsonify({"message": "Provider updated successfully"}), 200

# --- DELETE A PROVIDER ---
@providers_bp.route('/<int:id>', methods=['DELETE'])
def delete_provider(id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Providers WHERE ProviderID = %s", (id,))
    deleted_rows = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    if deleted_rows == 0:
        return jsonify({"error": "Provider not found"}), 404
    return jsonify({"message": "Provider deleted successfully"}), 200