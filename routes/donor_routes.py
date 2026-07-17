from flask import Blueprint, request, jsonify, current_app
import sqlite3
from datetime import date

donor_bp = Blueprint('donor', __name__)

@donor_bp.route('/register', methods=['POST'])
def register_donor():
    data = request.get_json()
    conn = current_app.config['MYSQL_OBJ']

    cursor = conn.cursor()

    query = """
        INSERT INTO Donors (user_id, name, age, blood_group, contact, last_donation)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (
        data['user_id'],
        data['name'],
        data['age'],
        data['blood_group'],
        data['contact'],
        data.get('last_donation')  # optional
    ))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Donor registered successfully'})



@donor_bp.route('/donate', methods=['POST'])
def donate_blood():
    data = request.get_json()
    conn = current_app.config['MYSQL_OBJ']

    # cursor = conn.cursor()
    cursor = conn.cursor()

    user_id = data.get('user_id')
    units = data.get('units_donated', 1)
    donation_date = data.get('donation_date', date.today())

    # ✅ Step 1: Get donor_id and blood_group using user_id
    cursor.execute("SELECT donor_id, blood_group FROM Donors WHERE user_id = ?", (user_id,))
    donor_info = cursor.fetchone()

    if not donor_info:
        cursor.close()
        return jsonify({'message': 'Donor not found for this user ID'}), 404

    donor_id = donor_info['donor_id']
    blood_group = donor_info['blood_group']

    # ✅ Step 2: Insert donation record
    insert_query = """
        INSERT INTO BloodDonations (donor_id, donation_date, units_donated)
        VALUES (?, ?, ?)
    """
    cursor.execute(insert_query, (donor_id, donation_date, units))

    # ✅ Step 3: Update BloodInventory
    update_query = """
        UPDATE BloodInventory
        SET units_available = units_available + ?
        WHERE blood_group = ?
    """
    cursor.execute(update_query, (units, blood_group))

    # ✅ Step 4: Update last_donation in Donors table
    cursor.execute(
        "UPDATE Donors SET last_donation = ? WHERE donor_id = ?",
        (donation_date, donor_id)
    )

    conn.commit()
    cursor.close()

    return jsonify({'message': 'Donation recorded and inventory updated'})

@donor_bp.route("/donations/<int:donor_id>", methods=["GET"])
def get_donation_history(donor_id):
    try:
        conn = current_app.config['MYSQL_OBJ']

        # cursor = conn.cursor()
        cur = conn.cursor()

        cur.execute(
            "SELECT donation_date, units_donated FROM BloodDonations WHERE donor_id = ? ORDER BY donation_date DESC",
            (donor_id,)
        )
        donations = cur.fetchall()
        cur.close()
        # conn.close()

        return jsonify({"success": True, "donations": donations})
    except Exception as e:
        print(f"Error fetching donation history: {e}")
        return jsonify({"success": False, "message": "Failed to fetch donation history"}), 500
    

@donor_bp.route('/get/<int:user_id>', methods=['GET'])
def get_donor_by_user_id(user_id):
    conn = current_app.config['MYSQL_OBJ']

    # cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute("SELECT donor_id FROM Donors WHERE user_id = ?", (user_id,))
    donor = cursor.fetchone()
    # cursor.close()
    if donor:
        return jsonify(donor)
    else:
        return jsonify({'message': 'Donor not found'}), 404