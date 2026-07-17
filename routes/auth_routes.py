from flask import Blueprint, request, jsonify, current_app
import sqlite3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400

    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    query = "SELECT * FROM Users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        user_data = {
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role']
        }
        return jsonify({'success': True, 'user': user_data})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
