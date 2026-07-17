from flask import Blueprint, request, jsonify, current_app
from datetime import date

recipient_bp = Blueprint('recipient', __name__)

@recipient_bp.route('/register', methods=['POST'])
def register_recipient():
    data = request.get_json()
    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    query = """
        INSERT INTO Recipients (user_id, name, age, blood_group, contact)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        data['user_id'],
        data['name'],
        data['age'],
        data['blood_group'],
        data['contact']
    ))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Recipient registered successfully'})

@recipient_bp.route('/request', methods=['POST'])
def request_blood():
    data = request.get_json()
    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    query = """
        INSERT INTO Requests (recipient_id, blood_group, units_needed, request_date)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (
        data['recipient_id'],
        data['blood_group'],
        data['units_needed'],
        data.get('request_date', date.today())
    ))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Blood request submitted successfully'})

@recipient_bp.route('/get/<int:user_id>', methods=['GET'])
def get_recipient_by_user_id(user_id):
    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()
    cursor.execute("SELECT recipient_id FROM Recipients WHERE user_id = ?", (user_id,))
    recipient = cursor.fetchone()
    cursor.close()
    if recipient:
        return jsonify(recipient)
    else:
        return jsonify({'message': 'Recipient not found'}), 404
