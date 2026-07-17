import os
import sqlite3
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider
from db_config import init_sqlite

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, sqlite3.Row):
            return dict(obj)
        return super().default(obj)

# Serve static files from 'frontend' folder
app = Flask(__name__, static_folder='frontend', static_url_path='/')
app.json = CustomJSONProvider(app)
CORS(app)

# Initialize SQLite
sqlite_db = init_sqlite(app)
app.config['MYSQL_OBJ'] = sqlite_db

# Import and register blueprints
from routes.auth_routes import auth_bp
from routes.donor_routes import donor_bp
from routes.recipient_routes import recipient_bp
from routes.admin_routes import admin_bp
from routes.general_routes import general_bp
from routes.register_routes import register_bp   

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(donor_bp, url_prefix='/api/donor')
app.register_blueprint(recipient_bp, url_prefix='/api/recipient')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(general_bp, url_prefix='/api')
app.register_blueprint(register_bp)  

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return "Not Found", 404

if __name__ == '__main__':
    app.run(debug=True)
