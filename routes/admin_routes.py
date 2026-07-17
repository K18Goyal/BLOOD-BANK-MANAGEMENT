from flask import Blueprint, request, jsonify, current_app

admin_bp = Blueprint('admin', __name__)

# 1. Admin Dashboard Stats
@admin_bp.route('/dashboard_stats', methods=['GET'])
def dashboard_stats():
    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    # Total donors
    cursor.execute("SELECT COUNT(*) FROM Donors")
    total_donors = cursor.fetchone()[0]

    # Total units available
    cursor.execute("SELECT SUM(units_available) FROM BloodInventory")
    total_units = cursor.fetchone()[0] or 0

    # Pending requests
    cursor.execute("SELECT COUNT(*) FROM Requests WHERE status = 'pending'")
    pending_requests = cursor.fetchone()[0]

    cursor.close()
    return jsonify({
        'total_donors': total_donors,
        'total_units': total_units,
        'pending_requests': pending_requests
    })


# 2. Manage Blood Requests
@admin_bp.route('/requests', methods=['GET'])
def get_all_requests():
    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.request_id, u.username, rc.name, r.blood_group, r.units_needed, r.status, r.request_date
        FROM Requests r
        JOIN Recipients rc ON r.recipient_id = rc.recipient_id
        JOIN Users u ON rc.user_id = u.user_id
    """)
    requests = cursor.fetchall()
    cursor.close()
    return jsonify({'requests': requests})


@admin_bp.route('/update_request_status', methods=['POST'])
def update_request_status():
    data = request.get_json()
    request_id = data['request_id']
    new_status = data['status']

    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    cursor.execute("SELECT blood_group, units_needed FROM Requests WHERE request_id = ?", (request_id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({'message': 'Request not found'}), 404

    blood_group, units_needed = result

    if new_status.lower() == 'approved':
        cursor.execute("""
            UPDATE BloodInventory
            SET units_available = units_available - ?
            WHERE blood_group = ? AND units_available >= ?
        """, (units_needed, blood_group, units_needed))
        if cursor.rowcount == 0:
            return jsonify({'message': 'Not enough blood units available'}), 400

    cursor.execute("UPDATE Requests SET status = ? WHERE request_id = ?", (new_status, request_id))
    conn.commit()
    cursor.close()
    return jsonify({'message': f'Request {new_status} successfully'})


# 3. View All Users
@admin_bp.route('/users', methods=['GET'])
def view_all_users():
    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, email, role, registration_date
        FROM Users
    """)
    users = cursor.fetchall()
    cursor.close()
    return jsonify({'users': users})



@admin_bp.route('/all_users', methods=['GET'])
def get_all_users():
    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.user_id, u.username AS name, 
           CASE 
             WHEN d.donor_id IS NOT NULL THEN 'Donor'
             WHEN r.recipient_id IS NOT NULL THEN 'Recipient'
             ELSE 'Unknown'
           END AS role,
           COALESCE(d.blood_group, r.blood_group) AS blood_group,
           COALESCE(d.contact, r.contact) AS contact
    FROM Users u
    LEFT JOIN Donors d ON u.user_id = d.user_id
    LEFT JOIN Recipients r ON u.user_id = r.user_id
""")

    users = cursor.fetchall()
    cursor.close()
    return jsonify({'users': users})


# 4. Blood Inventory Display and Update
@admin_bp.route('/inventory', methods=['GET'])
def get_inventory():
    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM BloodInventory")
    inventory = cursor.fetchall()
    cursor.close()
    return jsonify({'inventory': inventory})


@admin_bp.route('/update_inventory', methods=['POST'])
def update_inventory():
    try:
        data = request.get_json()
        blood_group = data['blood_group']
        units = data['units_available']

        conn = current_app.config['MYSQL_OBJ']
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO BloodInventory (blood_group, units_available)
            VALUES (?, ?)
            ON DUPLICATE KEY UPDATE units_available = VALUES(units_available)
        """, (blood_group, units))

        conn.commit()
        cursor.close()
        return jsonify({'message': f'Inventory updated for {blood_group}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@admin_bp.route('/donation_history', methods=['GET'])
def donation_history():
    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bd.donation_date, bd.units_donated,
               d.name AS donor_name, d.blood_group, d.contact
        FROM BloodDonations bd
        JOIN Donors d ON bd.donor_id = d.donor_id
        ORDER BY bd.donation_date DESC
    """)
    donations = cursor.fetchall()
    cursor.close()
    return jsonify({'donations': donations})

