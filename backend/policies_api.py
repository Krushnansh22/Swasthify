# File: Swasthify/backend/policies_api.py

from flask import Blueprint, request, jsonify
import db
import psycopg2

policies_bp = Blueprint('policies_bp', __name__)

# --- GET ALL POLICIES ---
@policies_bp.route('/', methods=['GET'])
def get_policies():
    conn = db.get_db_connection()
    cursor = db.get_dict_cursor(conn)
    cursor.execute("SELECT * FROM Policies ORDER BY PolicyID")
    policies = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(row) for row in policies]), 200

# --- CREATE A NEW POLICY ---
@policies_bp.route('/', methods=['POST'])
def create_policy():
    data = request.json
    conn = db.get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO Policies (PolicyName, Description, CoverageLimit, MonthlyPremium, Deductible)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING PolicyID;
    """
    cursor.execute(query, (
        data['PolicyName'], data.get('Description'), data.get('CoverageLimit'),
        data.get('MonthlyPremium'), data.get('Deductible')
    ))
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Policy created", "PolicyID": new_id}), 201

# --- GET A SINGLE POLICY ---
@policies_bp.route('/<int:id>', methods=['GET'])
def get_policy_by_id(id):
    conn = db.get_db_connection()
    cursor = db.get_dict_cursor(conn)
    cursor.execute("SELECT * FROM Policies WHERE PolicyID = %s", (id,))
    policy = cursor.fetchone()
    cursor.close()
    conn.close()
    if policy:
        return jsonify(dict(policy)), 200
    else:
        return jsonify({"error": "Policy not found"}), 404

# --- UPDATE A POLICY ---
@policies_bp.route('/<int:id>', methods=['PUT'])
def update_policy(id):
    data = request.json
    conn = db.get_db_connection()
    cursor = conn.cursor()
    query = """
        UPDATE Policies
        SET PolicyName = %s, Description = %s, CoverageLimit = %s,
            MonthlyPremium = %s, Deductible = %s
        WHERE PolicyID = %s
    """
    cursor.execute(query, (
        data['PolicyName'], data.get('Description'), data.get('CoverageLimit'),
        data.get('MonthlyPremium'), data.get('Deductible'), id
    ))
    updated_rows = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    if updated_rows == 0:
        return jsonify({"error": "Policy not found"}), 404
    return jsonify({"message": "Policy updated successfully"}), 200

# --- DELETE A POLICY ---
@policies_bp.route('/<int:id>', methods=['DELETE'])
def delete_policy(id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Policies WHERE PolicyID = %s", (id,))
    deleted_rows = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    if deleted_rows == 0:
        return jsonify({"error": "Policy not found"}), 404
    return jsonify({"message": "Policy deleted successfully"}), 200