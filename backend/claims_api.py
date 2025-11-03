# File: Swasthify/backend/claims_api.py

from flask import Blueprint, request, jsonify
import db
import psycopg2

claims_bp = Blueprint('claims_bp', __name__)

# --- GET ALL CLAIMS (with JOINs) ---
@claims_bp.route('/', methods=['GET'])
def get_claims():
    conn = db.get_db_connection()
    cursor = db.get_dict_cursor(conn)
    # This query joins tables to get meaningful names, not just IDs
    query = """
        SELECT 
            c.ClaimID, c.DateOfService, c.AmountBilled, c.AmountPaid, c.Status,
            p.ProviderName,
            ph.FirstName, ph.LastName
        FROM Claims c
        JOIN Providers p ON c.ProviderID = p.ProviderID
        JOIN PolicyEnrollments pe ON c.EnrollmentID = pe.EnrollmentID
        JOIN PolicyHolders ph ON pe.PolicyHolderID = ph.PolicyHolderID
        ORDER BY c.DateOfService DESC
    """
    cursor.execute(query)
    claims = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(row) for row in claims]), 200

# --- CREATE A NEW CLAIM (Provider action) ---
@claims_bp.route('/', methods=['POST'])
def create_claim():
    data = request.json
    conn = db.get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO Claims (EnrollmentID, ProviderID, DateOfService, DiagnosisCode, Description, AmountBilled, Status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
        RETURNING ClaimID;
    """
    try:
        cursor.execute(query, (
            data['EnrollmentID'], data['ProviderID'], data['DateOfService'],
            data.get('DiagnosisCode'), data.get('Description'), data['AmountBilled']
        ))
        new_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Claim submitted successfully", "ClaimID": new_id}), 201
    except (Exception, psycopg2.Error) as error:
        print(f"Error creating claim: {error}")
        return jsonify({"error": "Failed to submit claim. Check foreign keys (EnrollmentID, ProviderID)."}), 400
    finally:
        cursor.close()
        conn.close()

# --- GET A SINGLE CLAIM (with details) ---
@claims_bp.route('/<int:id>', methods=['GET'])
def get_claim_by_id(id):
    conn = db.get_db_connection()
    cursor = db.get_dict_cursor(conn)
    # More detailed query for a single claim
    query = """
        SELECT 
            c.*, 
            p.ProviderName,
            ph.FirstName, ph.LastName, ph.Email,
            pol.PolicyName, pol.CoverageLimit, pol.Deductible
        FROM Claims c
        JOIN Providers p ON c.ProviderID = p.ProviderID
        JOIN PolicyEnrollments pe ON c.EnrollmentID = pe.EnrollmentID
        JOIN PolicyHolders ph ON pe.PolicyHolderID = ph.PolicyHolderID
        JOIN Policies pol ON pe.PolicyID = pol.PolicyID
        WHERE c.ClaimID = %s
    """
    cursor.execute(query, (id,))
    claim = cursor.fetchone()
    cursor.close()
    conn.close()
    if claim:
        return jsonify(dict(claim)), 200
    else:
        return jsonify({"error": "Claim not found"}), 404

# --- PROCESS A CLAIM (Admin action: Approve/Deny) ---
@claims_bp.route('/<int:id>', methods=['PUT'])
def process_claim(id):
    data = request.json
    # Admin must provide the new 'Status' and 'AmountPaid'
    new_status = data.get('Status')
    amount_paid = data.get('AmountPaid')

    if new_status not in ['Approved', 'Denied', 'Processing']:
        return jsonify({"error": "Invalid status value."}), 400

    conn = db.get_db_connection()
    cursor = conn.cursor()
    query = """
        UPDATE Claims
        SET Status = %s, AmountPaid = %s
        WHERE ClaimID = %s
    """
    cursor.execute(query, (new_status, amount_paid, id))
    updated_rows = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    
    if updated_rows == 0:
        return jsonify({"error": "Claim not found"}), 404
    return jsonify({"message": "Claim processed successfully"}), 200

# --- DELETE A CLAIM ---
@claims_bp.route('/<int:id>', methods=['DELETE'])
def delete_claim(id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Claims WHERE ClaimID = %s", (id,))
    deleted_rows = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    if deleted_rows == 0:
        return jsonify({"error": "Claim not found"}), 404
    return jsonify({"message": "Claim deleted successfully"}), 200