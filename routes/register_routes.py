# routes/register_routes.py

from flask import Blueprint, request, jsonify, current_app

register_bp = Blueprint('register', __name__)

@register_bp.route('/api/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    conn = current_app.config['MYSQL_OBJ']
    cursor = conn.cursor()

    # Check if username exists
    cursor.execute("SELECT user_id FROM Users WHERE username = ?", (data['username'],))
    if cursor.fetchone():
        cursor.close()
        return jsonify({"error": "Username already taken"}), 400

    # Insert user if not exists
    cursor.execute(
        "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
        (data['username'], data['password'], data['role'])
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    return jsonify({"message": "User registered", "user_id": user_id})
