from flask import Blueprint, jsonify, current_app

general_bp = Blueprint('general', __name__)

@general_bp.route('/blood_inventory', methods=['GET'])
def show_inventory():
    conn = current_app.config['MYSQL_OBJ'].connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BloodInventory")
    inventory = cursor.fetchall()
    cursor.close()
    return jsonify({'inventory': inventory})
